# Test Cases — claude_playwrite

One-line test cases covering the onboarding form and all Playwright automation scripts.

---

## Form — Step Navigation

- `TC-01` Opening `http://localhost:8080` displays Step 1 (first name) centered on a dark gradient background.
- `TC-02` The progress bar shows a visible sliver (~7%) on Step 1, confirming it is active from the start.
- `TC-03` Typing text in the first name field and pressing Enter advances to Step 2 without clicking the button.
- `TC-04` Clicking the "Next →" button on any step advances to the next step.
- `TC-05` Each step transition plays a slide-up and fade-in animation lasting ~450ms.
- `TC-06` The step counter label (e.g. "3 / 12") updates correctly on every step.
- `TC-07` The progress bar width increases with each step and reaches 100% on the thank-you screen.
- `TC-08` Confirming the submission review displays the thank-you screen with a checkmark icon.
- `TC-09` Clicking "Start over" on the thank-you screen resets all inputs and returns to Step 1.

---

## Form — Keyboard Shortcuts

- `TC-10` Pressing Enter on a text input (`type="text"`) advances to the next step.
- `TC-11` Pressing Enter on a tel input (`type="tel"`) advances to the next step.
- `TC-12` Pressing Enter on a date input (`type="date"`) advances to the next step.
- `TC-13` Pressing Enter inside a textarea inserts a newline and does NOT advance the step.
- `TC-14` Pressing Ctrl+Enter inside a textarea advances to the next step.
- `TC-15` Pressing Meta+Enter (Cmd+Enter on Mac) inside a textarea also advances the step.
- `TC-16` Pressing Enter while a `<select>` is focused does NOT call tryAdvance — the browser handles the dropdown natively.

---

## Form — Submission Review

- `TC-64` Completing Step 12 displays a review screen before submission.
- `TC-65` The review screen lists every question, its saved answer, and "Not provided" for skipped optional answers.
- `TC-66` Clicking an answer's "Edit" button returns to its populated form step; "Confirm & submit" then displays the thank-you screen.

---

## Form — Validation

- `TC-17` Clicking "Next" on a required text field with no value shows a red error message below the button.
- `TC-18` The input shakes (CSS shake animation) when a required field fails validation.
- `TC-19` After a validation failure, typing valid input and pressing Enter clears the error and advances.
- `TC-20` Skipping the phone field (Step 3, optional) by pressing Enter advances without an error.
- `TC-21` Entering fewer than 7 characters in the phone field shows a "valid phone number" error.
- `TC-22` Entering a valid phone number (e.g. "+1 (555) 000-0000") passes validation and advances.
- `TC-23` Skipping the referral field (Step 8, optional) by pressing Enter advances without an error.
- `TC-24` Skipping the date field (Step 11, optional) by clicking Next advances without an error.
- `TC-25` Skipping the final textarea (Step 12, optional) via Ctrl+Enter advances without an error.

---

## Form — Optional Field Indicators

- `TC-26` Step 3 (phone) displays an "OPTIONAL" badge inline with the question label.
- `TC-27` Step 8 (referral) displays an "OPTIONAL" badge inline with the question label.
- `TC-28` Step 11 (date) displays an "OPTIONAL" badge inline with the question label.
- `TC-29` Step 12 (final textarea) displays an "OPTIONAL" badge inline with the question label.
- `TC-30` Required steps (1, 2, 4, 5, 6, 7, 9, 10) do NOT show an "OPTIONAL" badge.

---

## Form — Select Steps

- `TC-31` Step 6 (industry) shows a dropdown with 7 options plus a "Choose one…" placeholder.
- `TC-32` Step 7 (team size) shows a dropdown with 6 size-range options plus a "Choose one…" placeholder.
- `TC-33` The hint text on select steps reads "Choose an option, then click Next" (not "Press Enter").
- `TC-34` Selecting an option from a dropdown and clicking "Next →" advances to the next step.
- `TC-35` Clicking "Next →" on a required select with no option chosen shows a validation error.

---

## Form — Design / Layout

- `TC-36` The card uses a frosted-glass effect (backdrop-filter blur) on the dark gradient background.
- `TC-37` The input field shows a purple focus ring when clicked or tabbed into.
- `TC-38` At 390px viewport width the "Next →" button stretches to full card width.
- `TC-39` Question text scales responsively between 1.35rem (mobile) and 1.9rem (desktop) using clamp().
- `TC-40` The progress bar is fixed at the top of the viewport and stays visible during scrolling.
- `TC-41` The thank-you screen displays a gradient checkmark icon, "You're all set!" heading, and a "Start over" button.

---

## Playwright Script — automate_form.py

- `TC-42` Running `python3 scripts/automate_form.py` (with server running) opens a visible browser window.
- `TC-43` The script fills all 12 form steps in sequence without any assertion failures.
- `TC-44` After step 12, the script asserts the review screen contains all 12 answers, confirms submission, then asserts `.step--thankyou.is-active .thankyou-title` is visible.
- `TC-45` The script saves a screenshot of the completed form to `screenshots/form_completed.png`.
- `TC-46` The script clicks "Start over" and asserts the step counter returns to "1 / 12".
- `TC-47` Text inputs are filled using `.fill(value)` then advanced with `keyboard.press("Enter")`.
- `TC-48` Select inputs are filled using `.select_option(label=value)` then advanced via `.btn-next` click.
- `TC-49` Textarea inputs are filled using `.fill(value)` then advanced with `keyboard.press("Control+Enter")`.
- `TC-50` Date inputs are filled using `.fill("YYYY-MM-DD")` then advanced via `.btn-next` click.
- `TC-51` The script waits 550ms between each step to allow the 450ms CSS transition to complete.

---

## Playwright Script — screenshot.py

- `TC-52` Running `python3 scripts/screenshot.py https://example.com out.png` saves a full-page PNG to `out.png`.
- `TC-53` Omitting the output filename argument defaults to `screenshot.png` in the current directory.
- `TC-54` Running without any arguments prints the usage string and exits with code 1.
- `TC-55` The script uses `wait_until="networkidle"` to ensure dynamic content has loaded before capture.
- `TC-56` The screenshot is taken at a 1280×800 viewport.

---

## Playwright Script — automate.py

- `TC-57` Running `python3 scripts/automate.py` opens a visible Chromium window navigated to Hacker News.
- `TC-58` The script prints up to 10 story titles from the `.titleline > a` selector.
- `TC-59` A screenshot of the Hacker News page is saved to `screenshots/hn.png`.
- `TC-60` The browser stays open until the user presses Enter in the terminal (manual inspection pause).

---

## Dev Server

- `TC-61` Running `python3 -m http.server 8080` from the repo root serves `index.html` at `http://localhost:8080`.
- `TC-62` `styles.css` and `app.js` are served with HTTP 200 from the same root.
- `TC-63` No build step or compilation is required — the app runs directly from source files.
