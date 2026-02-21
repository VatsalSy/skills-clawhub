# Amber Voice Assistant - Setup Wizard Demo

This directory contains demo recordings of the interactive setup wizard.

## Files

### `demo.gif` (156 KB)
Animated GIF showing the complete setup wizard flow. Use this for:
- GitHub README embeds
- Documentation
- Quick previews

**Example usage in Markdown:**
```markdown
![Setup Wizard Demo](demo/demo.gif)
```

### `demo.cast` (9 KB)
Asciinema recording file. Use this for:
- Web embeds with asciinema player
- Higher quality playback
- Smaller file size

**Play locally:**
```bash
asciinema play demo.cast
```

**Embed on web:**
```html
<script src="https://asciinema.org/a/14.js" id="asciicast-14" async></script>
```

**Upload to asciinema.org:**
```bash
asciinema upload demo.cast
```

## What the Demo Shows

The wizard guides users through:

1. **Twilio Configuration**
   - Account SID validation (must start with "AC")
   - Real-time credential testing via Twilio API
   - Phone number format validation (E.164)

2. **OpenAI Configuration**
   - API key validation via OpenAI API
   - Optional project ID and webhook secret
   - Voice selection (alloy/echo/fable/onyx/nova/shimmer)

3. **Server Setup**
   - Port configuration
   - Automatic ngrok detection and tunnel discovery
   - Public URL configuration

4. **Optional Integrations**
   - OpenClaw gateway (brain-in-loop features)
   - Assistant personalization (name, operator info)
   - Call screening customization

5. **Post-Setup**
   - Automatic dependency installation
   - TypeScript build
   - Clear next steps with webhook URL

## Demo Flow

The demo uses these example values (not real credentials):
- **Twilio SID:** AC1234567890abcdef1234567890abcd
- **Phone:** +15551234567
- **OpenAI Key:** sk-proj-demo...
- **Assistant:** Amber
- **Operator:** John Smith
- **Organization:** Acme Corp

## Recreation

To record your own demo:

```bash
# Install dependencies
brew install asciinema agg expect

# Record with expect script
asciinema rec your-demo.cast --command "expect demo.exp"

# Convert to GIF
agg --font-size 14 --speed 2 --cols 80 --rows 30 your-demo.cast your-demo.gif
```

---

*Demo created on 2026-02-20 using asciinema 3.1.0 and agg 1.7.0*
