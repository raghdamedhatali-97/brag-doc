# Reminder setup

A skill only runs when the user opens a chat, so it cannot start a conversation on its own. Reminders come from outside the skill. There are two options.

## Option A: Claude Code routine (smart reminders)

The routine checks whether today's entry exists and only reminds the user if it does not. It stays silent on non-working days and during a pause.

Needs: a paid Claude plan with Claude Code, and the Google Drive and Gmail connectors enabled for the routine.

### Schedule

Run at 19:00, 20:00, 21:00 and 22:00 on working days, in the user's time zone.

Example cron for Sunday to Thursday, 19:00 to 22:00 local time:

```
0 19-22 * * 0-4
```

Check which time zone the scheduler uses. If it runs in UTC, convert: for Riyadh (UTC+3), 19:00-22:00 local is `0 16-19 * * 0-4` in UTC.

### Routine prompt

Paste this as the routine's prompt:

```
You are my brag-doc reminder. Do not chat; just do the check and stop.

1. In Google Drive, find the folder "Brag Doc" and read the latest "00 - Settings" file for my email, working days and time zone.
2. Work out today's date and the current hour in my time zone.
3. Stop without doing anything if any of these are true:
   - today is not one of my working days
   - a file titled "PAUSE <start> to <end>" covers today and there is no matching "(cancelled)" file
   - a file whose title starts with today's date and contains "Brag Entry" exists in the folder
4. Otherwise, send ONE email to my own address only (from Settings), never to anyone else:
   - Subject at 19:00: "Brag Doc: 3 minutes for today?"
   - Subject at 20:00 or later: "Brag Doc reminder (N of 3)"
   - Body: "Open Claude and say: log my day. It takes 3 minutes. Off today? Reply in Claude: skip today."
```

The skill's "never send email" rule covers emails to the manager. This routine only emails the user themself.

### Optional: weekly draft

A second routine on the weekly update day (for example Thursday 16:00 local) can run:

```
Use the brag-doc skill: create my weekly summary for my manager as a Gmail draft. Do not send it.
```

## Option B: Calendar reminder (no Claude Code needed)

1. In Google Calendar (or Outlook), create an event "Brag Doc - log my day", 19:00, 5 minutes.
2. Repeat: every weekday on your working days.
3. Add notifications: at the start, and after 60, 120 and 180 minutes (use "custom" notifications; some apps only allow notifications before the event, in which case create 4 events at 19:00, 20:00, 21:00 and 22:00).
4. In the event description, put: "Open Claude and say: log my day".

Limitation: calendar reminders fire even after you have answered. Dismiss them, or delete that day's later events.
