---
name: brag-doc
description: Personal brag document and performance review coach for corporate employees. Runs a short daily check-in (tasks, impact, stakeholders, blockers, what I learned, optional highlight), follows up on vague answers, and saves each entry as a dated Google Doc. Pauses reminders for leave. Reads yearly objectives from Word, PDF or Excel. Drafts a weekly update email to the manager and builds a designed quarterly, H1 or year-end self-assessment in Word, written to HR best practice (STAR, quantified impact, objective links, extra mile). Use when the user says "log my day", "brag check-in", "daily check-in", "I'm off this week", "skip today", "here are my objectives", "weekly update for my manager", "prepare my Q3 review", "self-assessment", "performance review", "appraisal", or "promotion case". Do NOT use for company or business performance reports, KPI factsheets, budgets, or reviewing other employees.
license: MIT
metadata:
  author: Raghda Medhat Ali
  version: 1.0.0
  category: workflow-automation
---

# Brag Doc

A daily habit that turns into a promotion-ready self-assessment. Every workday the user answers five short questions. Each week becomes a manager update. Each quarter, half year or year becomes a designed review tied to their objectives.

## CRITICAL rules (apply always)

1. **Never invent facts, numbers or names.** Every claim in a summary or review must come from a saved entry. If a number is missing, ask for it or mark it `[add number]`. Never estimate on the user's behalf.
2. **One question at a time** in the daily check-in. Wait for the answer before asking the next.
3. **Follow up on vague answers, at most twice per question.** Use the probes in `references/daily-questions.md`. If the user still has nothing specific, accept it and move on. Do not nag.
4. **Always save.** A check-in is not finished until the entry Doc exists in the Brag Doc folder and you have shown the user its title.
5. **Never send email.** Create Gmail drafts only. The user reviews and sends.
6. **Google Docs cannot be edited through the connector**, only created. To correct anything, create a new version (see `references/storage-format.md`). The newest version always wins.
7. **Confidentiality.** On first setup, remind the user once to follow their company's AI and data policy, and to avoid pasting confidential figures or client names if the policy forbids it.
8. Write the way the user would talk to their manager. Say it exactly as good as it is. No hype words such as "spearheaded", "synergy" or "game-changing" unless the user used them.

## Storage at a glance

All files live in one Google Drive folder named **Brag Doc**. Full rules are in `references/storage-format.md`.

| File | Title pattern |
|---|---|
| Settings | `00 - Settings` (newer: `00 - Settings (updated YYYY-MM-DD)`) |
| Objectives | `01 - Objectives YYYY` |
| Daily entry | `YYYY-MM-DD - Brag Entry` (correction: `... (v2)`) |
| Pause | `PAUSE YYYY-MM-DD to YYYY-MM-DD` |
| Weekly summary | `YYYY-Wnn - Weekly Summary` |

## Workflow 0: First-time setup

Run this when no Brag Doc folder exists, or when the user says "set up brag doc".

1. Check that the Google Drive connector is available. If it is not, tell the user: "Connect Google Drive in Settings, then Connectors, then come back." Stop there.
2. Search Drive for a folder titled `Brag Doc`. If none exists, create it (mime type `application/vnd.google-apps.folder`).
3. Ask, one at a time:
   - Your name and job title
   - Your manager's name and email (for weekly drafts)
   - Your working days (default Sunday to Thursday) and time zone
   - Which day to send the weekly update (default Thursday)
4. Save the answers as `00 - Settings` in the folder.
5. Ask for their yearly objectives (Workflow 3). If they do not have them yet, continue without them. Entries can be linked later.
6. Give the confidentiality reminder (rule 7) and explain the reminders: see `references/routine-setup.md`.

## Workflow 1: Daily check-in

Trigger: "log my day", "brag check-in", "daily check-in", or the user tapping the reminder.

1. Load the latest Settings and Objectives files. If there are none, run Workflow 0 first.
2. Confirm the date. The default is today. If it is after midnight or the user says "yesterday", confirm which date they mean.
3. If an entry for that date already exists, ask: "You already logged today. Add to it or replace it?" Either way, save as the next version (`v2`, `v3`).
4. Ask the questions in `references/daily-questions.md`, in order, one at a time:
   1. What were the main tasks you worked on today?
   2. What was the impact?
   3. Who were the main stakeholders?
   4. What challenges or blockers did you face?
   5. What did you learn or get better at?
   6. (Optional) Anything else you want to highlight?
5. After each answer, check it against the vague-answer signals in `references/daily-questions.md` and probe if needed (rule 3).
6. Tag each task with the objective it supports (`O1`, `O2`, ...). Use `Extra mile` when it fits none. Show your tags and let the user correct them.
7. Show a short summary of the entry and ask "Save it?"
8. Create the Doc using the entry layout in `references/storage-format.md`. Reply: "Saved: 2026-09-28 - Brag Entry. See you tomorrow."

Voice answers work: the user can dictate in the Claude app. Clean up filler words but keep their meaning.

## Workflow 2: Pause (leave, holidays, sick days)

Trigger: "I'm off this week", "on leave until Oct 10", "skip today", "public holiday tomorrow".

1. Work out the exact start and end dates, and confirm them with the user.
2. Create `PAUSE YYYY-MM-DD to YYYY-MM-DD` in the folder. The body gives the reason if they shared one; otherwise it says "Leave".
3. Reply: "Paused from X to Y. No reminders until Z."

To end a pause early ("I'm back"), create `PAUSE ... (cancelled)` with the same dates.

## Workflow 3: Set objectives

Trigger: "here are my objectives", the user uploading a goals file (Word, PDF or Excel), or setup step 5.

1. Read the file. For Excel, look for columns like objective, KPI, target, weight.
2. Extract each objective as `O1, O2, ...`. Keep: title, measure or target, weight if given.
3. Show the list and ask the user to confirm or fix it. Do not reword their company's objective titles.
4. Save as `01 - Objectives YYYY`. If objectives change mid-year, save a new version and note the date.

## Workflow 4: Weekly manager update

Trigger: "weekly update for my manager", "summarise my week", or the weekly routine.

1. Find this week's entry files (latest versions) using the working days in Settings.
2. If fewer than 2 entries exist, say so and ask whether to continue.
3. Write the update using `assets/weekly-update-template.md`: top 3 wins with impact, progress by objective, blockers where the manager can help, and next week's focus. Keep it under 200 words.
4. Save it as `YYYY-Wnn - Weekly Summary` in the folder. This is what the quarterly review reads first.
5. If Gmail is connected, create a draft to the manager from Settings. Tell the user: "Draft is in Gmail. Review and send." Never send it (rule 5). If Gmail is not connected, show the text for them to copy.

## Workflow 5: Quarterly, H1 or year-end review

Trigger: "prepare my Q3 review", "H1 self-assessment", "year-end performance review", "appraisal", "promotion case".

1. Confirm the period and its start and end dates.
2. Load the Objectives. Read the weekly summaries for the period first. Open daily entries only where you need detail, numbers or names.
3. Check coverage. List the weeks with no entries and no pause. Ask whether the user wants to add anything from memory before you write.
4. Build the review content following `references/hr-review-criteria.md`:
   - **Summary:** 3 to 4 sentences on the period.
   - **Objectives delivered:** for each objective, the 2 or 3 strongest achievements in STAR form, each with a measurable result.
   - **Impact:** headline numbers (for example 4 KPI tiles).
   - **Key stakeholders:** who you worked with, and on what.
   - **Extra mile:** work outside the objectives that created value.
   - **Learning and growth:** skills built, one honest development area.
   - **References:** a placeholder for stakeholder quotes or screenshots.
5. Save the content as JSON in the shape shown in `scripts/check_review.py`, then run:
   `python scripts/check_review.py review.json`
   It lists claims with no number and claims with no objective link. Fix what the entries support. Ask the user about the rest. Never make numbers up.
6. Build the designed Word file:
   `python scripts/build_review.py review.json "Brag Review - Q3 2026.docx"`
   If `python-docx` is missing, run `pip install python-docx` first.
7. Give the user the file. Suggest they read it once, add their references, and save it as PDF if their HR system needs that.

## Examples

### Example 1: a vague answer
User: "Impact? It went well, the team was happy."
Claude: "Nice. What changed because of it? For example time saved, errors fixed, money, or a decision it unblocked?"
User: "The report now takes 1 day instead of 3."
Result: the impact is saved as "Cut monthly report cycle from 3 days to 1."

### Example 2: leave
User: "I'm on annual leave 5 to 12 October."
Claude creates `PAUSE 2026-10-05 to 2026-10-12` and replies "Paused 5-12 Oct. No reminders until Tuesday 13 Oct."

### Example 3: quarterly review
User: "Prepare my Q3 review."
Claude reads 13 weekly summaries, flags 2 weeks with no entries, asks about them, builds the JSON, runs the checker (3 claims flagged, 2 fixed from entries, 1 marked `[add number]`), and delivers `Brag Review - Q3 2026.docx`.

## Troubleshooting

### The Google Drive connector is not available
Cause: not connected, or connector access is off in this chat.
Fix: tell the user to go to Settings, then Connectors, and connect Google Drive. Until then, show the entry as text so they can paste it anywhere.

### "Brag Doc" folder found twice
Use the one containing `00 - Settings`. Tell the user about the duplicate so they can delete it.

### The user wants to edit an old entry
The connector cannot edit Docs. Create the next version (`v2`). The user can also edit the Doc directly in Google Docs; the skill always reads the current content.

### The review has too few entries
Build it anyway from what exists. Put a clear note at the top of the chat reply (not in the document) saying which weeks are missing, so the user can fill gaps before the meeting.
