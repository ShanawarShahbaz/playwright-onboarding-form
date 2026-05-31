# Prompt Log — claude_playwrite

A record of every prompt given during this project's development, what was built, and what the outcome was.

---

## Prompt 1 — Install Playwright and set up browser automation

**Prompt:**
> "I want to use playwright CLI in order to do some browser automation stuff, whether that means testing out web apps or taking screenshots of things. Whatever the case, I just need you to figure out how you can install this for me and then go ahead and build a plan and lets do it."

**What was done:**
- Detected Python 3.9 available, no Node.js → chose Playwright for Python
- Ran `pip3 install playwright` (installed v1.60.0)
- Ran `playwright install chromium` to download browser binaries
- Created two starter scripts in the project root

**Files created:**
- `screenshot.py` — CLI utility: takes a headless full-page screenshot of any URL and saves it as a PNG
- `automate.py` — Demo script: opens a visible Chromium browser, navigates to Hacker News, scrapes top 10 story titles, saves a screenshot

**Commands to run:**
```bash
python3 screenshot.py https://example.com out.png
python3 automate.py
```

---

## Prompt 2 — Create CLAUDE.md project overview

**Prompt:**
> "Create claude.md file for the overview of this project."

**What was done:**
- Read all existing files to understand the project
- Created a project documentation file in the root

**Files created:**
- `CLAUDE.md` — covers setup instructions, script usage, key Playwright patterns, common wait strategies, and output file behavior

---

## Prompt 3 — Build a multi-page onboarding form web app

**Prompt:**
> "I need you to build me a form submission website now. I want this to basically be one page per question. As soon as I open up the page, it should ask me for my first name, and then there should be a button that prompts me to hit enter. When I hit enter, I go to the next page, and then I have my last name, my phone number, my business, and maybe, let's just say, eight questions about me, kind of getting me onboarded into this fake business or whatever. I just want to do this to see and test the functionality of what you're able to build me here. I still want it to look nice, so use the frontend design skill, but help me build out this plan so that you know exactly how we can actually execute on this."

**Plan approved, then built:**
- Pure vanilla JavaScript app (no framework, no npm, no build step)
- 12 questions total, one per screen, slide-up animation between each
- Dark gradient background with frosted-glass card (glassmorphism)
- Progress bar at top, keyboard-first navigation (Enter to advance)
- Playwright Python test script to automate the whole form

**Files created:**
- `index.html` — HTML shell only; links CSS and JS
- `styles.css` — complete design system: gradient, frosted card, slide animations, responsive layout, validation shake
- `app.js` — all JavaScript: QUESTIONS array, DOM generation, step transitions, validation, keyboard handling
- `automate_form.py` — Playwright test: fills all 12 fields, asserts thank-you screen, saves screenshot, tests restart

**12 questions built:**

| # | Question | Type | Required |
|---|---|---|---|
| 1 | What's your first name? | text | Yes |
| 2 | And your last name? | text | Yes |
| 3 | What's the best number to reach you? | tel | No |
| 4 | What's your business called? | text | Yes |
| 5 | What's your role or job title? | text | Yes |
| 6 | Which industry are you in? | select | Yes |
| 7 | How large is your team? | select | Yes |
| 8 | How did you hear about us? | text | No |
| 9 | What's your biggest challenge right now? | textarea | Yes |
| 10 | What are your primary goals with us? | textarea | Yes |
| 11 | When are you looking to get started? | date | No |
| 12 | Anything else you'd like us to know? | textarea | No |

**Commands to run:**
```bash
python3 -m http.server 8080   # open http://localhost:8080
python3 automate_form.py       # automated test (server must be running)
```

---

## Prompt 4 — Reorganize file structure for GitHub portfolio

**Prompt:**
> "What is best way to organize the file structure of this project, so that I am push it to git, and show it as portfolio."

**Plan approved (user clarified: build using JavaScript, use Playwright Python for testing), then executed:**

**Files moved:**
- `screenshot.py`, `automate.py`, `automate_form.py` → `scripts/` subfolder
- `form_completed.png` → `screenshots/` subfolder (portfolio preview image)
- `example_test.png`, `hn.png` → deleted (covered by .gitignore going forward)

**Files created:**
- `README.md` — full portfolio README with badges, embedded screenshot, live demo link placeholder, getting started guide, project structure
- `.gitignore` — excludes `__pycache__`, `.DS_Store`, all PNGs except `screenshots/form_completed.png`
- `requirements.txt` — pins `playwright==1.60.0`

**Path updates inside moved scripts:**
- `scripts/automate.py` — screenshot path updated: `hn.png` → `screenshots/hn.png`
- `scripts/automate_form.py` — screenshot path updated: `form_completed.png` → `screenshots/form_completed.png`
- `scripts/screenshot.py` — docstring usage line updated
- `CLAUDE.md` — all script paths and run commands updated; hardcoded local path removed

**Final directory tree:**
```
claude_playwrite/
├── index.html
├── styles.css
├── app.js
├── README.md
├── .gitignore
├── requirements.txt
├── CLAUDE.md
├── scripts/
│   ├── automate_form.py
│   ├── automate.py
│   └── screenshot.py
└── screenshots/
    └── form_completed.png
```

**To push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: Playwright onboarding form"
git remote add origin <your-repo-url>
git push -u origin main
```

---

## Prompt 5 — Run app with headed browser, test it, find and fix bugs

**Prompt:**
> "Spin up the server so that you can actually run this app, then I want you to use your browser and test it out. Fill in the fields, click through and if there are any bugs or if there is anything wrong with the functionality of the site, make a note so that you can go ahead and fix the actual site itself. I also want you to do this in a headed browser so that I can watch what's going on."

**What was done:**
- Started HTTP server on port 8080
- Ran `scripts/automate_form.py` with `headless=False` so the browser was visible
- Took visual audit screenshots at 14 key states (each step type, validation state, mobile viewport, thank-you screen)
- Inspected every screenshot and analysed the code for UX/logic issues

**4 bugs found and fixed:**

| # | Bug | File | Fix |
|---|---|---|---|
| 1 | **Select + Enter conflict** — pressing Enter on a `<select>` called `tryAdvance()` instead of letting the browser open/confirm the dropdown | `app.js` | Added `if (focused.tagName === 'SELECT') return;` in keydown handler so browser handles Enter natively |
| 2 | **Wrong hint on select steps** — said "Press Enter ↵ or click Next" which was misleading since Enter didn't work reliably | `app.js` | `buildHint()` now returns "Choose an option, then click Next" for select type |
| 3 | **No optional indicator** — required and optional fields looked identical; users couldn't tell which steps to skip | `app.js` + `styles.css` | Added `OPTIONAL` badge inline with the question label on steps 3, 8, 11, 12 |
| 4 | **Progress bar invisible on step 1** — formula `(current / TOTAL) * 100` gave 0% on the very first question | `app.js` | Changed to `((current + 1) / (TOTAL + 1)) * 100` so bar shows ~7% immediately on load |

**Regression test:** After all fixes, full 12-step Playwright automation ran without errors and `screenshots/form_completed.png` was updated.
