# TixFlow - OpenClaw Skill

AI-powered event assistant skill for OpenClaw agents.

## Installation

```bash
clawhub install tixflow
```

Or manually:

```bash
cd skill
npm install
```

## Environment Variables

Create a `.env` file:

```env
GOOGLE_CALENDAR_API_KEY=your_google_api_key
KYD_API_KEY=your_kyd_api_key
```

## Functions

- `findEvents({type, location, date, budget})` - Search for events
- `getEventDetails(eventId)` - Get event information
- `purchaseTicket({eventId, quantity, walletAddress})` - Buy tickets
- `syncToCalendar({eventId, userEmail})` - Sync to Google Calendar
- `addToWaitlist({eventId, walletAddress, notificationMethod})` - Join waitlist
- `checkPrices(eventId)` - Compare prices across platforms

## Demo Mode

Without API keys, the skill runs in demo mode with mock event data.

## License

MIT
