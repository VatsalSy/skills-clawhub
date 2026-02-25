#!/usr/bin/env python3
"""
Doubao (豆包) Seed-ASR 2.0 — audio file transcription.

API docs: https://www.volcengine.com/docs/6561/1354868
Endpoint: https://openspeech.bytedance.com/api/v3/auc/bigmodel/
Auth: X-Api-App-Key + X-Api-Access-Key
Resource-Id: volc.seedasr.auc

Audio upload: The Doubao API requires a publicly accessible URL.
This script uploads audio to Volcengine TOS (object storage) by default,
keeping data within Volcengine infrastructure.
Set DOUBAO_ASR_UPLOAD_URL to use a custom upload endpoint instead.
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import quote, urlparse

try:
    import requests
except ImportError:
    sys.exit("requests is required: pip install requests")

SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
RESOURCE_ID = "volc.seedasr.auc"

FORMAT_MAP = {
    ".m4a": "m4a",
    ".mp3": "mp3",
    ".mp4": "mp4",
    ".wav": "wav",
    ".ogg": "ogg",
    ".flac": "flac",
}

MIME_MAP = {
    "m4a": "audio/mp4",
    "mp3": "audio/mpeg",
    "mp4": "audio/mp4",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
}

# --- TOS presigned URL upload (default) ---

TOS_REGION = os.environ.get("VOLCENGINE_TOS_REGION", "cn-beijing")
TOS_ENDPOINT = os.environ.get(
    "VOLCENGINE_TOS_ENDPOINT",
    f"https://tos-{TOS_REGION}.volces.com",
)
TOS_BUCKET = os.environ.get("VOLCENGINE_TOS_BUCKET", "")


def _tos_sign_v4(method: str, url: str, ak: str, sk: str,
                 region: str, headers: dict, expires: int = 3600) -> str:
    """Generate a Volcengine TOS V4 presigned URL (query-string auth)."""
    parsed = urlparse(url)
    now = datetime.now(timezone.utc)
    date_stamp = now.strftime("%Y%m%d")
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    credential_scope = f"{date_stamp}/{region}/tos/request"
    signed_headers = "host"
    canonical_headers = f"host:{parsed.hostname}\n"

    # Build canonical query string
    query_params = {
        "X-Tos-Algorithm": "TOS4-HMAC-SHA256",
        "X-Tos-Credential": f"{ak}/{credential_scope}",
        "X-Tos-Date": amz_date,
        "X-Tos-Expires": str(expires),
        "X-Tos-SignedHeaders": signed_headers,
    }
    canonical_qs = "&".join(
        f"{quote(k, safe='')}={quote(v, safe='')}"
        for k, v in sorted(query_params.items())
    )

    canonical_request = "\n".join([
        method,
        quote(parsed.path, safe="/"),
        canonical_qs,
        canonical_headers,
        signed_headers,
        "UNSIGNED-PAYLOAD",
    ])

    string_to_sign = "\n".join([
        "TOS4-HMAC-SHA256",
        amz_date,
        credential_scope,
        hashlib.sha256(canonical_request.encode()).hexdigest(),
    ])

    def _sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    signing_key = _sign(
        _sign(
            _sign(
                _sign(sk.encode("utf-8"), date_stamp),
                region,
            ),
            "tos",
        ),
        "request",
    )
    signature = hmac.new(
        signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return f"{parsed.scheme}://{parsed.hostname}{parsed.path}?{canonical_qs}&X-Tos-Signature={signature}"


def upload_to_tos(filepath: str, fmt: str) -> str:
    """Upload audio to Volcengine TOS and return a presigned GET URL."""
    ak = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
    sk = os.environ.get("VOLCENGINE_SECRET_ACCESS_KEY", "")
    bucket = TOS_BUCKET

    if not ak or not sk or not bucket:
        missing = []
        if not ak:
            missing.append("VOLCENGINE_ACCESS_KEY_ID")
        if not sk:
            missing.append("VOLCENGINE_SECRET_ACCESS_KEY")
        if not bucket:
            missing.append("VOLCENGINE_TOS_BUCKET")
        sys.exit(
            f"Missing: {', '.join(missing)}\n\n"
            "The Doubao ASR API requires audio via URL. This skill uploads to\n"
            "Volcengine TOS (object storage) — your audio stays within Volcengine.\n\n"
            "Setup (3 steps):\n"
            "  1. Create IAM Access Key: https://console.volcengine.com/iam/keymanage/\n"
            "  2. Create TOS Bucket: https://console.volcengine.com/tos/bucket/create\n"
            "  3. Set env vars:\n"
            "     export VOLCENGINE_ACCESS_KEY_ID='your_ak'\n"
            "     export VOLCENGINE_SECRET_ACCESS_KEY='your_sk'\n"
            "     export VOLCENGINE_TOS_BUCKET='your_bucket_name'\n\n"
            "Alternative: set DOUBAO_ASR_UPLOAD_URL to use your own upload endpoint."
        )

    object_key = f"doubao-asr/{uuid.uuid4()}.{fmt}"
    put_url_raw = f"{TOS_ENDPOINT}/{bucket}/{object_key}"
    content_type = MIME_MAP.get(fmt, "application/octet-stream")

    put_url = _tos_sign_v4("PUT", put_url_raw, ak, sk, TOS_REGION, {
        "Content-Type": content_type,
    }, expires=300)

    with open(filepath, "rb") as f:
        resp = requests.put(put_url, data=f, headers={
            "Content-Type": content_type,
        }, timeout=120)
    if resp.status_code not in (200, 201):
        sys.exit(f"TOS upload failed ({resp.status_code}): {resp.text[:200]}")

    get_url = _tos_sign_v4("GET", put_url_raw, ak, sk, TOS_REGION, {},
                           expires=3600)
    return get_url


def upload_custom(filepath: str) -> str:
    """Upload to a user-specified endpoint (POST multipart, returns URL)."""
    upload_url = os.environ["DOUBAO_ASR_UPLOAD_URL"]
    with open(filepath, "rb") as f:
        resp = requests.post(upload_url, files={"files[]": f}, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get("files"):
        return data["files"][0]["url"]
    if isinstance(data, dict) and data.get("url"):
        return data["url"]
    sys.exit(f"Custom upload response unrecognized: {json.dumps(data)[:200]}")


def upload_audio(filepath: str, fmt: str) -> str:
    """Upload audio file and return an accessible URL."""
    custom_url = os.environ.get("DOUBAO_ASR_UPLOAD_URL", "")
    if custom_url:
        print(f"  Uploading to custom endpoint...", file=sys.stderr)
        return upload_custom(filepath)
    else:
        print(f"  Uploading to Volcengine TOS...", file=sys.stderr)
        return upload_to_tos(filepath, fmt)


# --- Doubao ASR API ---

def get_headers(request_id: str, sequence: int | None = -1) -> dict:
    app_id = os.environ.get("VOLCENGINE_APP_ID", "")
    token = os.environ.get("VOLCENGINE_ACCESS_TOKEN", "")
    if not app_id or not token:
        sys.exit("Missing VOLCENGINE_APP_ID or VOLCENGINE_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": token,
        "X-Api-Resource-Id": RESOURCE_ID,
        "X-Api-Request-Id": request_id,
    }
    if sequence is not None:
        headers["X-Api-Sequence"] = str(sequence)
    return headers


def submit(audio_url: str, fmt: str, speakers: bool = False) -> str:
    """Submit a transcription task. Returns request_id."""
    request_id = str(uuid.uuid4())
    headers = get_headers(request_id, sequence=-1)
    body = {
        "user": {"uid": "openclaw-doubao-asr"},
        "audio": {"url": audio_url, "format": fmt},
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
            "enable_ddc": True,
            "show_utterances": True,
        },
    }
    if speakers:
        body["request"]["enable_speaker_info"] = True

    resp = requests.post(SUBMIT_URL, headers=headers, json=body, timeout=30)
    status = resp.headers.get("X-Api-Status-Code", "")
    message = resp.headers.get("X-Api-Message", "")
    if status != "20000000":
        sys.exit(f"Submit failed: {status} {message}")
    return request_id


def poll(request_id: str, timeout: int = 600, interval: int = 3) -> dict:
    """Poll until the task completes. Returns the full result dict."""
    headers = get_headers(request_id, sequence=None)
    elapsed = 0
    while elapsed < timeout:
        resp = requests.post(QUERY_URL, headers=headers, json={}, timeout=30)
        status = resp.headers.get("X-Api-Status-Code", "")
        if status == "20000000":
            return resp.json()
        if status in ("20000001", "20000002"):
            print(f"\r  Transcribing... ({elapsed}s)", end="", file=sys.stderr)
            time.sleep(interval)
            elapsed += interval
            continue
        if status == "20000003":
            print("\n  Silent audio, no transcript.", file=sys.stderr)
            return {"result": {"text": "", "utterances": []}}
        message = resp.headers.get("X-Api-Message", "")
        sys.exit(f"Query failed: {status} {message}")
    sys.exit(f"Timeout after {timeout}s")


def main():
    parser = argparse.ArgumentParser(description="Doubao Seed-ASR 2.0 transcription")
    parser.add_argument("audio", help="Path to audio file (or URL)")
    parser.add_argument("--format", dest="fmt", help="Audio format (auto-detected from extension)")
    parser.add_argument("--out", help="Output file path (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output full JSON result")
    parser.add_argument("--speakers", action="store_true", help="Enable speaker diarization")
    parser.add_argument("--timeout", type=int, default=600, help="Max wait seconds (default: 600)")
    args = parser.parse_args()

    # Support direct URL input (skip upload)
    if args.audio.startswith("http://") or args.audio.startswith("https://"):
        audio_url = args.audio
        fmt = args.fmt
        if not fmt:
            ext = os.path.splitext(urlparse(audio_url).path)[1].lower()
            fmt = FORMAT_MAP.get(ext)
        if not fmt:
            sys.exit("Cannot detect format from URL. Use --format to specify.")
    else:
        if not os.path.isfile(args.audio):
            sys.exit(f"File not found: {args.audio}")
        ext = os.path.splitext(args.audio)[1].lower()
        fmt = args.fmt or FORMAT_MAP.get(ext)
        if not fmt:
            sys.exit(f"Unknown audio format: {ext}. Use --format to specify.")
        audio_url = upload_audio(args.audio, fmt)

    # Submit task
    print("  Submitting transcription task...", file=sys.stderr)
    request_id = submit(audio_url, fmt, speakers=args.speakers)

    # Poll for result
    data = poll(request_id, timeout=args.timeout)
    print("", file=sys.stderr)  # newline after progress

    result = data.get("result", {})
    text = result.get("text", "")

    # Output
    if args.json:
        output = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        output = text

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
        print(args.out)
    else:
        print(output)


if __name__ == "__main__":
    main()
