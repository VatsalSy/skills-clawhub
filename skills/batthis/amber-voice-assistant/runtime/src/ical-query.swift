import EventKit
import Foundation

let store = EKEventStore()
let semaphore = DispatchSemaphore(value: 0)

// Request calendar access
if #available(macOS 14.0, *) {
    store.requestFullAccessToEvents { granted, error in
        if !granted {
            print("ERROR: Calendar access denied. Grant in System Settings > Privacy > Calendars.")
            if let e = error { print("Detail: \(e.localizedDescription)") }
        }
        semaphore.signal()
    }
} else {
    store.requestAccess(to: .event) { granted, error in
        if !granted {
            print("ERROR: Calendar access denied.")
        }
        semaphore.signal()
    }
}
semaphore.wait()

let args = CommandLine.arguments

func printUsage() {
    print("Usage: ical-query <command> [options]")
    print("")
    print("  calendars                        List all calendars")
    print("  today                            Events for today")
    print("  tomorrow                         Events for tomorrow")
    print("  week                             Events for the next 7 days")
    print("  range <start> <end>              Events in date range (YYYY-MM-DD)")
    print("  add <title> <start> <end>        Create event (YYYY-MM-DDTHH:MM)")
    print("      [--calendar <name>]          Calendar name (default: Abe)")
    print("      [--location <loc>]           Location")
    print("      [--notes <notes>]            Notes")
    print("      [--allday]                   All-day event (start/end as YYYY-MM-DD)")
    print("  delete <event-id>                Delete event by ID")
}

guard args.count >= 2 else {
    printUsage()
    exit(1)
}

let command = args[1]
let df = DateFormatter()
df.dateFormat = "yyyy-MM-dd"
df.timeZone = TimeZone.current

let tf = DateFormatter()
tf.dateFormat = "yyyy-MM-dd HH:mm"
tf.timeZone = TimeZone.current

let dtf = DateFormatter()
dtf.dateFormat = "yyyy-MM-dd'T'HH:mm"
dtf.timeZone = TimeZone.current

func startOfDay(_ date: Date) -> Date {
    Calendar.current.startOfDay(for: date)
}

func endOfDay(_ date: Date) -> Date {
    Calendar.current.date(byAdding: .day, value: 1, to: startOfDay(date))!
}

func printEvents(from start: Date, to end: Date) {
    let calendars = store.calendars(for: .event)
    let predicate = store.predicateForEvents(withStart: start, end: end, calendars: calendars)
    let events = store.events(matching: predicate).sorted { $0.startDate < $1.startDate }

    if events.isEmpty {
        print("No events found.")
        return
    }

    for event in events {
        let startStr = tf.string(from: event.startDate)
        let endStr = tf.string(from: event.endDate)
        let cal = event.calendar.title
        let allDay = event.isAllDay ? " [all-day]" : ""
        let loc = event.location ?? ""
        let locStr = loc.isEmpty ? "" : " @ \(loc)"
        let eid = event.eventIdentifier ?? "?"
        print("\(startStr) - \(endStr) | \(event.title ?? "(no title)")\(allDay)\(locStr) [\(cal)] id:\(eid)")
    }
}

func findCalendar(named name: String) -> EKCalendar? {
    let calendars = store.calendars(for: .event)
    // Exact match first
    if let cal = calendars.first(where: { $0.title.lowercased() == name.lowercased() }) {
        return cal
    }
    // Partial match
    if let cal = calendars.first(where: { $0.title.lowercased().contains(name.lowercased()) }) {
        return cal
    }
    return nil
}

func getArg(flag: String) -> String? {
    guard let idx = args.firstIndex(of: flag), idx + 1 < args.count else { return nil }
    return args[idx + 1]
}

switch command {
case "calendars":
    let calendars = store.calendars(for: .event)
    for cal in calendars {
        print("\(cal.title) (source: \(cal.source.title))")
    }

case "today":
    let now = Date()
    printEvents(from: startOfDay(now), to: endOfDay(now))

case "tomorrow":
    let tomorrow = Calendar.current.date(byAdding: .day, value: 1, to: Date())!
    printEvents(from: startOfDay(tomorrow), to: endOfDay(tomorrow))

case "week":
    let now = Date()
    let weekEnd = Calendar.current.date(byAdding: .day, value: 7, to: now)!
    printEvents(from: startOfDay(now), to: endOfDay(weekEnd))

case "range":
    guard args.count >= 4,
          let start = df.date(from: args[2]),
          let end = df.date(from: args[3]) else {
        print("ERROR: range requires two dates in YYYY-MM-DD format")
        exit(1)
    }
    printEvents(from: startOfDay(start), to: endOfDay(end))

case "add":
    guard args.count >= 5 else {
        print("ERROR: add requires <title> <start> <end>")
        print("  Datetime format: YYYY-MM-DDTHH:MM (e.g. 2026-02-11T15:00)")
        print("  For all-day: YYYY-MM-DD with --allday flag")
        exit(1)
    }
    let title = args[2]
    let startStr = args[3]
    let endStr = args[4]
    let isAllDay = args.contains("--allday")
    let calName = getArg(flag: "--calendar") ?? "Abe"
    let location = getArg(flag: "--location")
    let notes = getArg(flag: "--notes")

    guard let calendar = findCalendar(named: calName) else {
        print("ERROR: Calendar '\(calName)' not found. Available:")
        for cal in store.calendars(for: .event) { print("  - \(cal.title)") }
        exit(1)
    }

    var startDate: Date?
    var endDate: Date?
    if isAllDay {
        startDate = df.date(from: startStr)
        endDate = df.date(from: endStr)
    } else {
        startDate = dtf.date(from: startStr)
        endDate = dtf.date(from: endStr)
    }

    guard let sd = startDate, let ed = endDate else {
        print("ERROR: Could not parse dates. Use YYYY-MM-DDTHH:MM (or YYYY-MM-DD with --allday)")
        exit(1)
    }

    let event = EKEvent(eventStore: store)
    event.title = title
    event.startDate = sd
    event.endDate = ed
    event.isAllDay = isAllDay
    event.calendar = calendar
    if let loc = location { event.location = loc }
    if let n = notes { event.notes = n }

    do {
        try store.save(event, span: .thisEvent)
        let outStart = isAllDay ? df.string(from: sd) : tf.string(from: sd)
        let outEnd = isAllDay ? df.string(from: ed) : tf.string(from: ed)
        print("OK: Created '\(title)' on \(outStart) - \(outEnd) [\(calendar.title)]")
        if let eid = event.eventIdentifier {
            print("Event ID: \(eid)")
        }
    } catch {
        print("ERROR: Failed to create event: \(error.localizedDescription)")
        exit(1)
    }

case "delete":
    guard args.count >= 3 else {
        print("ERROR: delete requires <event-id>")
        exit(1)
    }
    let eventId = args[2]
    guard let event = store.event(withIdentifier: eventId) else {
        print("ERROR: Event not found with ID: \(eventId)")
        exit(1)
    }
    do {
        try store.remove(event, span: .thisEvent)
        print("OK: Deleted '\(event.title ?? "(no title)")'")
    } catch {
        print("ERROR: Failed to delete event: \(error.localizedDescription)")
        exit(1)
    }

default:
    printUsage()
    exit(1)
}
