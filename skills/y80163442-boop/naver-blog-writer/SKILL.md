# Naver Blog Writer Skill Pack (MVP)

이 skill pack은 OpenClaw/Virtual ACP 환경에서 아래 흐름을 표준화합니다.

- `preflight(local daemon)`
- 실패 시 `RUNNER_NOT_READY + setup_url`
- `setup_runner` 실행
- 사람 1회 로그인
- `publish`

## Config

- `OPENCLAW_OFFERING_ID`: 기본 `naver-blog-writer`
- `X_LOCAL_TOKEN`: local daemon 인증 토큰 (`preflight`, `publish` 필수)
- setup_url 자동 발급 모드: `PROOF_TOKEN` + `SETUP_ISSUE_URL` 필요
- setup_url 사전 발급 모드: `SETUP_URL` 사용 시 proof 단계 생략 가능
- `LOCAL_DAEMON_PORT`: 기본 `19090`
- `DEVICE_FINGERPRINT`: 미지정 시 `hostname-platform-arch` 자동 생성

`publish` 실행 경로는 아래 둘 중 하나가 반드시 필요:

1. offering execute 경로  
   `OPENCLAW_OFFERING_EXECUTE_URL` (+ 필요 시 `OPENCLAW_CORE_API_KEY`)
2. direct dispatch fallback 경로  
   `CONTROL_PLANE_URL` + `ACP_ADMIN_API_KEY`

## Tools

### 1) preflight

```bash
tools/preflight \
  --proof-token "$PROOF_TOKEN" \
  --setup-issue-url "$SETUP_ISSUE_URL" \
  --local-daemon-port 19090 \
  --x-local-token "$X_LOCAL_TOKEN"
```

성공 시 local identity JSON을 반환합니다.
실패 시 반드시 아래 표준 에러를 반환합니다.

```json
{
  "error": "RUNNER_NOT_READY",
  "setup_url": "https://...",
  "next_action": "RUN_SETUP"
}
```

### 2) setup_runner

```bash
tools/setup_runner \
  --proof-token "$PROOF_TOKEN" \
  --setup-issue-url "$SETUP_ISSUE_URL" \
  --auto-service both
```

실행 후 로그인 1회 필요:

```bash
npx @y80163442/naver-thin-runner login
```

실행 모드:

- 상주(worker): `npx @y80163442/naver-thin-runner start`
- 요청당 종료(run-per-request): `npx @y80163442/naver-thin-runner start --once`

### 3) publish

```bash
tools/publish --title "제목" --body "본문" --tags "tag1,tag2"
```

동작:

1. preflight
2. `/v1/local/identity`
3. `/v1/local/seal-job`
4. offering execute 호출(또는 direct dispatch fallback)

## Notes

- 1차 지원 OS: macOS
- local daemon 접근 가능한 로컬 호스트 실행을 전제로 합니다.
- `start`가 종료되지 않는 것은 정상 동작입니다.
- OpenClaw/ACP 에이전트의 요청당 실행이 필요하면 `start --once`를 사용하세요.
