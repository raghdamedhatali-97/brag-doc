# Storage format

All data lives in one Google Drive folder named **Brag Doc**. The Google Drive connector can create files and read them, but cannot edit an existing file's content. So every change is a new file, and the newest version wins.

## File naming

| File | Title | Notes |
|---|---|---|
| Settings | `00 - Settings` | Newer versions: `00 - Settings (updated YYYY-MM-DD)`. Use the latest date. |
| Objectives | `01 - Objectives YYYY` | Newer versions: `01 - Objectives YYYY (updated YYYY-MM-DD)`. |
| Daily entry | `YYYY-MM-DD - Brag Entry` | Corrections or additions: `YYYY-MM-DD - Brag Entry (v2)`, `(v3)`. Use the highest version. |
| Pause | `PAUSE YYYY-MM-DD to YYYY-MM-DD` | Cancelled: `PAUSE YYYY-MM-DD to YYYY-MM-DD (cancelled)`. A cancelled pause overrides the matching pause. |
| Weekly summary | `YYYY-Wnn - Weekly Summary` | ISO week number, two digits (`2026-W39`). |

Dates are always `YYYY-MM-DD` so files sort correctly and the reminder routine can find today's entry by title.

Create every file as a Google Doc: `contentMimeType: text/plain` with the text below as `textContent`, and `parentId` set to the Brag Doc folder id.

## Settings layout

```
BRAG DOC SETTINGS
Name: Sara Ahmed
Job title: Senior FP&A Analyst
Manager: Omar Khalid
Manager email: omar@example.com
Working days: Sun, Mon, Tue, Wed, Thu
Time zone: Asia/Riyadh
Weekly update day: Thu
Created: 2026-09-28
```

## Objectives layout

```
OBJECTIVES 2026
Source file: 2026 Goals.xlsx

O1 | Reduce month-end close time | Target: 5 working days | Weight: 30%
O2 | Build 2027 budget model | Target: approved by Nov 30 | Weight: 40%
O3 | Improve forecast accuracy | Target: within 5% | Weight: 30%
```

## Daily entry layout

```
BRAG ENTRY - 2026-09-28 (Sun)

TASKS
- [O1] Automated the bank reconciliation for 3 accounts
- [Extra mile] Walked the sales ops team through the new dashboard

IMPACT
- [O1] Reconciliation now takes 2 hours instead of 1 day
- [Extra mile] Sales ops can pull their own numbers; 4 fewer requests to FP&A this week

STAKEHOLDERS
- Treasury team (Ali) - bank file formats
- Sales ops (2 analysts) - dashboard training

BLOCKERS
- Waiting on IT for bank API access; escalated to IT lead

LEARNED
- Power Query merge on fuzzy match

HIGHLIGHT
- Treasury head thanked me in the team channel

TAGS: O1, Extra mile
```

Leave out an empty section only for HIGHLIGHT. For others write "None".

## Pause layout

```
PAUSE
From: 2026-10-05
To: 2026-10-12
Reason: Annual leave
```

## Weekly summary layout

Use `assets/weekly-update-template.md`. Save the final text exactly as sent to the manager, so the quarterly review reads the same story.

## Finding things

- Folder: search for a folder titled `Brag Doc`. If there are two, use the one containing `00 - Settings`.
- Today's entry: search titles starting with today's date inside the folder.
- A period: list files in the folder and filter titles by date prefix. For a quarter, read the `Weekly Summary` files first, then open daily entries for detail.
