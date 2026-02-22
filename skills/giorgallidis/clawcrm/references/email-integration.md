# Email Integration Reference

## Option 1: OAuth (Recommended for End Users)

Zero-setup flow for ClawCRM users:

1. User clicks "Connect Email" → OAuth consent screen (Google or Microsoft)
2. Grant send + read permissions
3. ClawCRM sends from user's real email via Gmail API / Microsoft Graph
4. Replies land in user's inbox and are read via same OAuth token
5. Thread matching via Message-ID / In-Reply-To headers

**Benefits:** No DKIM/SPF setup, emails come from user's domain, replies thread naturally.

**Implementation:**
- Google: OAuth 2.0 → Gmail API (`gmail.send`, `gmail.readonly` scopes)
- Microsoft: OAuth 2.0 → Microsoft Graph (`Mail.Send`, `Mail.Read` scopes)
- Thread tracking: Store Message-ID per outreach, match replies by In-Reply-To header

## Option 2: MailerSend (Managed Sending)

For agents without user OAuth:

```bash
curl -X POST https://api.mailersend.com/v1/email \
  -H "Authorization: Bearer $(cat secrets/mailersend-api-key.txt)" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"email": "hello@yourdomain.com", "name": "Your Name"},
    "to": [{"email": "lead@example.com"}],
    "subject": "Subject line",
    "html": "<p>Email body</p>"
  }'
```

**Requirements:** Verified domain with DKIM + SPF records.

**Reply handling:** Route replies to a monitored inbox, poll via IMAP.

## Option 3: Himalaya/IMAP (Reading Replies)

For monitoring an inbox for lead replies:

```bash
# Search for replies from a specific lead
himalaya envelope list --account <account> from lead@example.com

# Read a specific email
himalaya message read <id> --account <account>

# Search by subject
himalaya envelope list --account <account> subject "Re: Your practice"
```

Configure accounts in `~/.config/himalaya/config.toml`.

## Thread Tracking Pattern

1. When sending outreach, store: lead_id, message_id, subject, timestamp
2. Periodically poll inbox for new messages
3. Match replies by In-Reply-To header or subject line + sender email
4. Update lead status and log touchpoint in ClawCRM
5. Flag high-priority replies (interested, meeting request) for human review
