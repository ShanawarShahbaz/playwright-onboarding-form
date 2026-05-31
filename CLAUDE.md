# claude_playwrite

Browser automation and screenshot project using **Playwright for Python**.

## Setup

Python 3.9 + pip. No Node.js required.

```bash
pip install -r requirements.txt
python3 -m playwright install chromium
```

## Onboarding Form App

A Typeform-style multi-step onboarding form (12 questions, one per screen, smooth slide animations).

**Stack:** Vanilla JS (`app.js`) + CSS (`styles.css`) + HTML shell (`index.html`). Zero dependencies — served by Python's built-in HTTP server.

**Run the app:**
```bash
python3 -m http.server 8080
# Open http://localhost:8080 in any browser
```

**Run the Playwright test (server must be running):**
```bash
python3 scripts/automate_form.py
```
The test fills all 12 fields automatically (visible browser), asserts the thank-you screen appears, saves `screenshots/form_completed.png`, and tests the restart flow.

---

## Scripts

### scripts/screenshot.py
Headless full-page screenshot of any URL.

```bash
python3 scripts/screenshot.py <url> [output.png]
python3 scripts/screenshot.py https://example.com screenshots/out.png
```

### scripts/automate.py
Interactive automation demo — opens a visible Chromium window, navigates to Hacker News, scrapes the top story titles, and saves a screenshot.

```bash
python3 scripts/automate.py
```

Set `headless=False` → `headless=True` to run without a visible browser.

## Key Playwright Patterns

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    page.goto("https://example.com", wait_until="networkidle")

    # Screenshot
    page.screenshot(path="screenshots/out.png", full_page=True)

    # Scrape text
    texts = page.locator("css-selector").all_text_contents()

    # Click / fill forms
    page.locator("input[name='q']").fill("search term")
    page.locator("button[type='submit']").click()

    browser.close()
```

## Common wait strategies

| Strategy | When to use |
|---|---|
| `wait_until="networkidle"` | Page with lots of async requests |
| `wait_until="domcontentloaded"` | Fast pages, static HTML |
| `page.wait_for_selector("css")` | Wait for a specific element to appear |
| `page.wait_for_load_state("networkidle")` | After navigation within a SPA |

## Output files

PNG screenshots are saved to `screenshots/` by default.
