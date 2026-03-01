---
name: icloud-toolkit
description: >
  Unified iCloud integration for Calendar, Email, and Contacts. Use when:
  (1) creating, listing, searching, or deleting calendar events, (2) reading,
  sending, or searching email, (3) looking up, creating, editing, or deleting
  contacts, (4) any task involving iCloud calendar, email, or contacts. Handles
  timezone conversion, iCloud-compatible formatting, and vdirsyncer sync
  automatically.
metadata:
  openclaw:
    emoji: "☁️"
    primaryEnv: "ICLOUD_APP_PASSWORD"
    install: ["brew install vdirsyncer", "brew install khal", "brew install himalaya", "brew install khard"]
    requires:
      bins: ["python3", "himalaya", "khal", "vdirsyncer", "khard"]
---

# iCloud Toolkit

Unified Calendar + Email + Contacts CLI. One script, all iCloud operations.

**Script:** `scripts/icloud.py`
**Config:** `config/config.json`

## First-Time Setup

When `config/config.json` is missing, the skill outputs `SETUP_REQUIRED` instead of running commands. Follow this two-step flow:

### Step 1: Configure (gather info + connect to iCloud)

Ask the user for:
1. **Apple ID** (iCloud login email — used for authentication)
2. **Sending address** (the From address for outgoing email — usually the same as Apple ID unless they have a custom domain)
3. **Display name** (for sent emails)
4. **Timezone** (IANA format like `America/New_York` — auto-detected if omitted)

Most users send from their Apple ID, so for step 2 just ask: "Is your sending address the same as your Apple ID, or do you use a custom domain?" If it's the same, omit `--apple-id`. Only users with iCloud custom domains (e.g., `you@yourdomain.com`) need `--apple-id` set separately.

The password is managed by OpenClaw's secrets system via `$ICLOUD_APP_PASSWORD`. If the user hasn't set it yet, tell them:
> You need an iCloud app-specific password. Go to https://appleid.apple.com → Sign-In and Security → App-Specific Passwords → Generate one for "iCloud Toolkit". Then set it with: `/secret set ICLOUD_APP_PASSWORD`

Then run:
```bash
# Most users (sending address = Apple ID):
python3 $ICLOUD setup configure --email APPLE_ID --name "USER_NAME" --timezone TIMEZONE

# Custom domain users (sending address differs from Apple ID):
python3 $ICLOUD setup configure --email SENDING_ADDRESS --apple-id APPLE_ID --name "USER_NAME" --timezone TIMEZONE
```

This writes the auth file, generates vdirsyncer config (CalDAV + CardDAV), runs discovery+sync, and **outputs discovered calendars and address books as JSON**.

### Step 2: Finalize (map calendars + address books + generate remaining configs)

Show the user the discovered calendars and address books from Step 1 output. Ask them to give each a friendly name (e.g., "Personal", "Work") and pick defaults.

Then run:
```bash
python3 $ICLOUD setup finalize --email SENDING_ADDRESS --apple-id APPLE_ID --name "USER_NAME" --timezone TIMEZONE \
  --calendars '{"Personal":"uuid-from-discovery","Work":"another-uuid"}' --default Personal \
  --addressbooks '{"Contacts":"uuid-from-discovery"}' --default-addressbook Contacts
```

This writes `config/config.json` (including `email_addresses` for reply-matching), generates khal, himalaya, and khard configs, and runs verification. The `--addressbooks` and `--default-addressbook` flags are optional — omit them to skip contacts setup.

## Quick Reference

```bash
ICLOUD=~/.openclaw/workspace/skills/icloud-toolkit/scripts/icloud.py

# Calendar
python3 $ICLOUD calendar list                                    # Today
python3 $ICLOUD calendar list --days 7                           # Next 7 days
python3 $ICLOUD calendar list --days 7 --calendar Appointments   # Specific calendar
python3 $ICLOUD calendar search "meeting"                        # Search events
python3 $ICLOUD calendar create <calendar> <date> <start> <end> <title> [--location] [--description]
python3 $ICLOUD calendar create-allday <calendar> <date> <title> [--description]
python3 $ICLOUD calendar delete <uid>                            # Delete by UID
python3 $ICLOUD calendar sync                                    # Manual sync

# Email
python3 $ICLOUD email list                                       # Latest 10
python3 $ICLOUD email list --count 20 --folder Sent              # Sent folder
python3 $ICLOUD email list --unread                              # Unread only
python3 $ICLOUD email read <id> [--folder X]                      # Read email (folder defaults to INBOX)
python3 $ICLOUD email send <to> <subject> <body>                 # Send email
python3 $ICLOUD email reply <id> <body> [--all] [--folder X]     # Reply (From auto-matched to whichever address received the original)
python3 $ICLOUD email search "from Apple" [--folder X]            # Search (folder defaults to INBOX)
python3 $ICLOUD email move <folder> <id> [--source X]             # Move email (source defaults to INBOX)
python3 $ICLOUD email delete <id> [--folder X]                   # Delete email (move to Deleted Messages)

# Folder
python3 $ICLOUD folder purge <folder>                            # Purge all emails from folder

# Contacts
python3 $ICLOUD contact list                                     # All contacts
python3 $ICLOUD contact list --addressbook Contacts --count 20   # Specific book, limit results
python3 $ICLOUD contact show <uid>                               # Show by UID
python3 $ICLOUD contact search "John"                            # Search contacts
python3 $ICLOUD contact create John Doe --email john@example.com --phone +15551234567
python3 $ICLOUD contact create --fn "Acme Corp" --org "Acme Corp"   # Org-only contact
python3 $ICLOUD contact edit <uid> --add-email second@example.com   # Add email to existing
python3 $ICLOUD contact edit <uid> --first Jane --last Smith        # Change name
python3 $ICLOUD contact delete <uid>                             # Delete by UID
python3 $ICLOUD contact sync                                     # Manual sync

# Setup
python3 $ICLOUD setup configure --email X --apple-id X --name X [--timezone X]   # Step 1: connect + discover
python3 $ICLOUD setup finalize --email X --apple-id X --name X --timezone X \
  --calendars '{"Name":"uuid"}' --default Name \
  [--addressbooks '{"Name":"uuid"}' --default-addressbook Name]                  # Step 2: write configs
python3 $ICLOUD setup verify                                        # Run smoke tests
python3 $ICLOUD setup init                                          # Interactive wizard (dev only)
python3 $ICLOUD setup discover-calendars                            # Show calendar mapping
```

## Calendar

### Creating Events

Times are **local** — the script handles UTC conversion automatically using the `timezone` field in `config/config.json`. DST is handled correctly for all timezones.

```bash
# Timed event
python3 $ICLOUD calendar create Appointments 2026-03-15 14:00 15:30 "Team Meeting" \
  --location "Board Room" --description "Weekly sync"

# All-day event
python3 $ICLOUD calendar create-allday General 2026-03-15 "Company Holiday"
```

**What happens internally:**
1. Syncs with iCloud (pull latest)
2. Converts local time → UTC (14:00 CST → 20:00 UTC)
3. Generates clean .ics with UTC timestamps (no VTIMEZONE — this is the fix for iCloud treating events as all-day)
4. Writes .ics to correct calendar directory
5. Syncs with iCloud (push changes)

### Listing Events

```bash
python3 $ICLOUD calendar list                     # Today only
python3 $ICLOUD calendar list --days 7            # Next 7 days
python3 $ICLOUD calendar list --calendar Social   # Only Social calendar
```

### Searching Events

```bash
python3 $ICLOUD calendar search "dentist"
python3 $ICLOUD calendar search "flight"
```

### Deleting Events

Get the UID from khal list output or from the create confirmation:
```bash
python3 $ICLOUD calendar delete abc12345-6789-...
```

### Calendar Names

| Name         | Purpose                        |
|--------------|--------------------------------|
| Social       | Social events, family, friends |
| Reminders    | Reminders                      |
| Appointments | Work/professional              |
| General      | Default catch-all              |

### Syncing

Sync happens automatically before reads and around writes. Manual sync:
```bash
python3 $ICLOUD calendar sync
```

## Email

### Listing Emails

```bash
python3 $ICLOUD email list                        # Latest 10
python3 $ICLOUD email list --count 20             # Latest 20
python3 $ICLOUD email list --folder "Sent Messages"  # Sent
python3 $ICLOUD email list --unread               # Unread only
```

### Reading Emails

```bash
python3 $ICLOUD email read 2541                   # Read by ID from list output
python3 $ICLOUD email read 1736 --folder "Deleted Messages"   # Read from non-INBOX folder
```

### Sending Emails

```bash
python3 $ICLOUD email send "recipient@example.com" "Subject line" "Body of the email"
```

**Default From address:** Emails are sent from the `account_email` field in `config/config.json`, NOT the iCloud login address used for IMAP/SMTP authentication. These are often different — iCloud lets users send from a custom domain while authenticating with their Apple ID. When previewing a draft for the user, always state the correct From address from `account_email`.

**IMPORTANT:** Always ask permission before sending emails on behalf of the user.

### Searching Emails

Uses himalaya query syntax (positional args):
```bash
python3 $ICLOUD email search "from Apple"
python3 $ICLOUD email search "subject invoice"
python3 $ICLOUD email search "after 2026-02-01"
python3 $ICLOUD email search "from Apple and after 2026-01-01"
python3 $ICLOUD email search "from Apple" --folder "Sent Messages"   # Search non-INBOX folder
```

### Moving Emails

```bash
python3 $ICLOUD email move "Deleted Messages" 2541
python3 $ICLOUD email move "Archive" 2541
python3 $ICLOUD email move INBOX 1736 --source "Deleted Messages"   # Restore from trash
```

**Note:** Argument order is `<folder> <id>` (folder first, same as himalaya). Without `--source`, moves default to INBOX as the source folder.

iCloud folders: INBOX, Sent Messages, Drafts, Deleted Messages, Junk, Archive

### Deleting Emails

```bash
python3 $ICLOUD email delete 2541                                # Delete from INBOX (default)
python3 $ICLOUD email delete 1736 --folder Junk                  # Delete from specific folder
```

## Folder Operations

### Purging a Folder

Permanently deletes all emails in a folder. The folder itself remains but is emptied.

```bash
python3 $ICLOUD folder purge "Junk"
python3 $ICLOUD folder purge "Deleted Messages"
```

This is non-interactive (no confirmation prompt), so always confirm with the user before purging.

## Contacts

### Listing Contacts

```bash
python3 $ICLOUD contact list                          # All contacts
python3 $ICLOUD contact list --count 20               # First 20
python3 $ICLOUD contact list --addressbook Contacts   # Specific address book
```

### Showing a Contact

```bash
python3 $ICLOUD contact show <uid>                    # By UID (direct file lookup)
python3 $ICLOUD contact show "John Doe"               # By name (khard search)
```

### Searching Contacts

```bash
python3 $ICLOUD contact search "John"
python3 $ICLOUD contact search "Acme"
```

### Creating Contacts

```bash
# Basic contact
python3 $ICLOUD contact create John Doe --email john@example.com --phone +15551234567

# Full contact
python3 $ICLOUD contact create John Doe \
  --email john@work.com --email john@home.com \
  --phone +15551234567 --phone +15559876543 \
  --org "Acme Corp" --title "Engineer" \
  --nickname "Johnny" --birthday 1990-01-15 \
  --note "Met at conference" --category friend

# Organization-only contact (no person name)
python3 $ICLOUD contact create --fn "Acme Corp" --org "Acme Corp" --phone +15551234567

# To a specific address book
python3 $ICLOUD contact create John Doe --email j@x.com --addressbook Work
```

**What happens internally:**
1. Syncs with iCloud (pulls latest — aborts if sync fails)
2. Generates vCard 3.0 with UUID
3. Writes `.vcf` to address book directory
4. Syncs with iCloud (pushes changes)

### Editing Contacts

```bash
# Change name
python3 $ICLOUD contact edit <uid> --first Jane --last Smith

# Add an email (non-destructive — keeps existing emails)
python3 $ICLOUD contact edit <uid> --add-email new@example.com

# Remove a specific email
python3 $ICLOUD contact edit <uid> --remove-email old@example.com

# Replace ALL emails (destructive)
python3 $ICLOUD contact edit <uid> --email only@example.com

# Add/remove phones work the same way
python3 $ICLOUD contact edit <uid> --add-phone +15559999999
python3 $ICLOUD contact edit <uid> --remove-phone +15551111111

# Update other fields
python3 $ICLOUD contact edit <uid> --org "New Corp" --title "Manager" --note "Promoted"
```

**Lossless editing:** When editing a contact, Apple-specific properties (X-ABLabel, X-APPLE-*, PHOTO, etc.) are preserved. The edit reads the existing vCard, modifies only the fields you specify, and writes back to the same file path (preserving vdirsyncer's filename mapping).

### Deleting Contacts

```bash
python3 $ICLOUD contact delete <uid>
```

Get the UID from `contact list` (UIDs shown in output) or from the `contact create` confirmation.

### Syncing

Sync happens automatically before reads and around writes. Manual sync:
```bash
python3 $ICLOUD contact sync
```

## Notes

- **Timezone:** Set `timezone` in `config/config.json` to your IANA timezone (e.g. `America/New_York`, `Europe/London`). All times you enter are local — the script converts, DST-aware.
- **Sync:** Automatic before reads, before+after writes. No need to sync manually.
- **Config:** `config/config.json` — calendar names, address book names, binary paths, timezone.
- **Auth:** Single password at `config/auth` — shared by himalaya, vdirsyncer, and khard (via vdirsyncer).
- **Self-test:** `python3 $ICLOUD --test` — verifies UTC conversion, .ics generation, and vCard generation/parsing.
- **First-time setup:** See the "First-Time Setup" section above.
