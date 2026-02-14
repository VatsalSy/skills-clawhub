# clawrtc

Mine RTC tokens on real hardware with your AI agent.

## What It Does

ClawRTC is the RustChain mining client — it lets any AI agent prove it controls real physical hardware and earn RTC (RustChain Token) rewards. Modern x86/ARM hardware earns at 1x rate. Vintage hardware (PowerPC G4/G5, IBM POWER8, Amiga, SPARC) earns 1.2x–2.5x through the Proof of Antiquity consensus mechanism.

## How It Works

1. **Install**: `clawrtc install --wallet my-agent` — extracts bundled Python miner scripts, creates a virtual environment
2. **Attest**: The miner contacts the RustChain network every few minutes, submitting hardware fingerprint data (CPU model, clock drift, cache timing, VM detection)
3. **Earn**: RTC tokens accumulate in your wallet each epoch (~10 minutes), weighted by your hardware's antiquity multiplier
4. **Bridge**: Convert RTC to wRTC (Solana SPL token) via bottube.ai/bridge, trade on Raydium DEX

## Commands

| Command | Description |
|---------|-------------|
| `clawrtc install` | Install miner, configure wallet, extract bundled scripts |
| `clawrtc install --dry-run` | Preview without installing (security audit) |
| `clawrtc install --verify` | Show SHA256 hashes of bundled files |
| `clawrtc start` | Start mining in foreground |
| `clawrtc start --service` | Start + create background systemd/launchd service |
| `clawrtc stop` | Stop mining |
| `clawrtc status` | Check miner, wallet, and network status |
| `clawrtc logs` | View miner output |
| `clawrtc uninstall` | Remove everything cleanly |

## Security

- All miner code is **bundled in the package** — no external downloads
- Network endpoint uses **CA-signed TLS certificate**
- `--dry-run` and `--verify` flags for auditing before install
- Interactive consent prompt before any files are extracted
- VM detection warns users that virtual machines earn near-zero rewards
- No personal data collected — only CPU model, timing variance, and architecture

## Hardware Multipliers

| Hardware | Multiplier |
|----------|-----------|
| PowerPC G4 | 2.5x |
| PowerPC G5 | 2.0x |
| PowerPC G3 | 1.8x |
| IBM POWER8 | 1.5x |
| Pentium 4 | 1.5x |
| Retro x86 | 1.4x |
| Apple Silicon | 1.2x |
| Modern x86_64 / ARM | 1.0x |
| Virtual Machine | ~0x |

## Requirements

- Node.js 14+ (for CLI)
- Python 3.8+ (for miner scripts)
- Linux or macOS
- Real hardware (VMs are detected and penalized)

## Links

- Source: https://github.com/Scottcjn/Rustchain
- PyPI: https://pypi.org/project/clawrtc/
- Explorer: https://rustchain.org
- Token: https://solscan.io/token/12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X
