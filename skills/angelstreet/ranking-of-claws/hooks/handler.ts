import { createHash } from "crypto";
import { hostname } from "os";

const API_URL = "https://rankingofclaws.angelstreet.io/api/report";

// In-memory accumulator
let tokensDelta = 0;
let tokensInDelta = 0;
let tokensOutDelta = 0;
let lastReportTime = 0;
const REPORT_INTERVAL_MS = 60 * 60 * 1000; // 1 hour

function getGatewayId(): string {
  const raw = `${hostname()}-${process.env.HOME || ""}-openclaw`;
  return createHash("sha256").update(raw).digest("hex").slice(0, 16);
}

function getAgentName(): string {
  return process.env.RANKING_AGENT_NAME || hostname() || "anonymous";
}

function getCountry(): string {
  return process.env.RANKING_COUNTRY || Intl.DateTimeFormat().resolvedOptions().timeZone?.split("/")[0] || "unknown";
}

async function report() {
  if (tokensDelta === 0) return;

  try {
    const body = {
      gateway_id: getGatewayId(),
      agent_name: getAgentName(),
      country: getCountry(),
      tokens_delta: tokensDelta,
      tokens_in_delta: tokensInDelta,
      tokens_out_delta: tokensOutDelta,
      model: "mixed",
    };

    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(10000),
    });

    if (res.ok) {
      tokensDelta = 0;
      tokensInDelta = 0;
      tokensOutDelta = 0;
      lastReportTime = Date.now();
    }
  } catch {
    // Silent fail — will retry next hour
  }
}

const handler = async (event: any) => {
  if (event.type !== "message" || event.action !== "sent") return;

  // Estimate tokens from content length (rough: 1 token ≈ 4 chars)
  const content = event.context?.content || "";
  const estimatedTokens = Math.ceil(content.length / 4);
  tokensOutDelta += estimatedTokens;
  tokensDelta += estimatedTokens;

  // Report if enough time has passed
  if (Date.now() - lastReportTime >= REPORT_INTERVAL_MS) {
    void report();
  }
};

export default handler;
