---
name: clawcrm
description: "Manage leads, outreach campaigns, analytics, and email follow-ups using ClawCRM — the AI-native CRM. Use when the agent needs to: manage a sales pipeline (create/read/update leads), run outreach campaigns and email sequences, check pipeline analytics and conversion metrics, send or draft personalized emails to leads, handle email replies and follow-ups, configure quiz funnels or proposal pages, or any CRM/sales operations. Requires a ClawCRM deployment URL and admin token."
---

# ClawCRM — AI-Native CRM Skill

ClawCRM is a CRM built for AI agents to operate autonomously. It manages leads, campaigns, outreach, analytics, quizzes, and proposals via a REST API.

## Setup

The agent needs two things configured in TOOLS.md:

```markdown
### ClawCRM
- Base URL: https://<deployment>.netlify.app (or self-hosted URL)
- Auth Header: x-admin-token: <token>
- Token file: secrets/clawcrm-token.txt
```

All API calls use:
```bash
curl -s "$BASE_URL/api/openclaw/<endpoint>" -H "x-admin-token: $(cat secrets/clawcrm-token.txt)"
```

## Core Operations

### Leads

```bash
# List leads (paginated)
GET /api/openclaw/leads?limit=100&offset=0

# Create lead (with optional custom fields)
POST /api/openclaw/leads
{"email":"...", "firstName":"...", "lastName":"...", "clinicName":"...", "practiceType":"...", "customFields":{"annual_revenue":"500k","referral_source":"linkedin"}}

# Update lead (with optional custom fields)
PUT /api/openclaw/leads
{"id":"...", "status":"qualified", "customFields":{"insurance_type":"commercial"}}

# Lead fields: id, email, clinicName, practiceType, tier (high/mid/low), status (new/prospect/contacted/qualified/won/lost), quizAnswers, score, crmData (includes custom fields)
```

### Pipeline Stages

```bash
# List pipeline stages
GET /api/openclaw/stages

# Create stage
POST /api/openclaw/stages
{"name":"Discovery", "order":1, "color":"#3B82F6", "isDefault":false}

# Update stage
PUT /api/openclaw/stages
{"id":"...", "name":"Qualified Lead", "order":2}

# Delete stage
DELETE /api/openclaw/stages?id=<stage_id>
```

### Custom Fields

```bash
# List custom fields
GET /api/openclaw/fields

# Create custom field
POST /api/openclaw/fields
{"fieldName":"annual_revenue","fieldLabel":"Annual Revenue","fieldType":"text","order":1,"isRequired":false}

# fieldType options: text, number, date, select, multiselect, boolean
# For select/multiselect: include "options": ["Option 1", "Option 2"]

# Update custom field
PUT /api/openclaw/fields
{"id":"...", "fieldLabel":"Annual Revenue (USD)", "isRequired":true}

# Delete custom field
DELETE /api/openclaw/fields?id=<field_id>
```

### Org Settings

```bash
# Get org settings (branding, contact, locale, features)
GET /api/openclaw/org

# Update org settings (full replace)
PUT /api/openclaw/org
{"branding":{"brandName":"Acme Corp","primaryColor":"#FF6B35"},"contact":{"replyToEmail":"hello@acme.com"}}

# Partial update (merge with existing)
PATCH /api/openclaw/org
{"branding":{"logoUrl":"https://example.com/logo.png"}}

# Settings structure:
# - branding: brandName, logoUrl, primaryColor, secondaryColor
# - contact: replyToEmail, fromName, supportEmail, phone
# - locale: timezone, currency, dateFormat
# - features: quizEnabled, proposalsEnabled, analyticsEnabled, emailIntegrationEnabled
```

### Campaign Templates

```bash
# List campaign templates (org-specific + public)
GET /api/openclaw/templates?category=<category>&include_public=true

# Create campaign template
POST /api/openclaw/templates
{"name":"Welcome Sequence","category":"onboarding","trigger":"quiz_completed","steps":[{"channel":"email","delay":0,"subject":"...","body":"..."}]}

# Instantiate template as campaign
PATCH /api/openclaw/templates
{"templateId":"...", "name":"Q1 Welcome Campaign"}

# Categories: onboarding, nurture, reactivation, winback, custom
# Steps: [{"channel":"email|sms","delay":<hours>,"subject":"...","body":"..."}]
```

### Analytics

```bash
# Pipeline overview (default 30d)
GET /api/openclaw/analytics

# Returns: totalLeads, leadsInPeriod, quizCompletions, proposalsViewed, conversionRate, leadsWon, pipeline byStatus
```

### Campaigns & Sequences

```bash
# List campaigns
GET /api/openclaw/campaigns

# Create campaign sequence
POST /api/openclaw/campaigns
{"name":"...", "trigger":"quiz_completed|high_score_lead|manual|...", "steps":[...]}

# Triggers: quiz_completed, proposal_viewed, proposal_not_viewed_24h, high_score_lead, stage_changed, manual
# Channels: email, sms, linkedin, twitter
```

### Follow-ups

```bash
# Get actionable follow-ups with email templates
GET /api/openclaw/followups

# Send follow-up
POST /api/openclaw/followups
{"leadId":"...", "channel":"email", "subject":"...", "body":"..."}
```

### Touchpoints

```bash
# Lead activity history
GET /api/openclaw/touchpoints?leadId=<id>

# Log touchpoint
POST /api/openclaw/touchpoints
{"leadId":"...", "type":"email|call|meeting|note", "content":"..."}
```

### Other Endpoints

```bash
GET /api/openclaw/health          # Health check
GET /api/openclaw/quiz            # Quiz funnel config
GET /api/openclaw/playbooks       # SDR workflow playbooks
GET /api/config/proposal          # Proposal page config
```

## Email Integration

For sending outreach emails, ClawCRM works with external email providers:

- **MailerSend** — API-based transactional email (configure API key + verified domain)
- **Himalaya/IMAP** — Read replies, search threads, manage inbox
- **Gmail/Outlook OAuth** — Zero-setup for end users (connect via OAuth, send from their real email)

See `references/email-integration.md` for setup patterns.

## Outreach Workflow

1. Pull leads: `GET /api/openclaw/leads` → filter by tier/status
2. Draft personalized emails using lead data (quiz answers, practice type, pain points)
3. Save drafts for human review before sending
4. Send via MailerSend or follow-up endpoint
5. Log touchpoints: `POST /api/openclaw/touchpoints`
6. Monitor replies via IMAP and update lead status
7. Check analytics: `GET /api/openclaw/analytics`

See `references/outreach-playbook.md` for creative outreach strategies.

## Key Principles

- **Outcomes over output** — 100 leads in a spreadsheet is worthless if nobody's been contacted. Measure by replies, meetings booked, deals closed.
- **Always personalize** — Use quiz answers, practice type, location, and pain points. Never send generic templates.
- **Human-in-the-loop for sends** — Draft emails and save to a file for review. Only send after approval unless explicitly told to auto-send.
- **Log everything** — Every email sent, reply received, meeting booked → log as touchpoint.
