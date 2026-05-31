"""
Playwright test: drives all 12 steps of the onboarding form automatically.

Prerequisites:
  python3 -m http.server 8080   (run from repo root, in a separate terminal)

Usage:
  python3 scripts/automate_form.py
"""
from playwright.sync_api import sync_playwright

TEST_DATA = [
    ("text",     "Jane"),
    ("text",     "Doe"),
    ("tel",      "+1 (555) 123-4567"),
    ("text",     "Acme Corp"),
    ("text",     "Head of Product"),
    ("select",   "Technology / SaaS"),
    ("select",   "11–50"),
    ("text",     "A friend recommended you"),
    ("textarea", "We struggle with lead conversion at the bottom of the funnel."),
    ("textarea", "Increase MRR, reduce churn, and ship faster."),
    ("date",     "2025-09-01"),
    ("textarea", "Looking forward to working together!"),
]

TOTAL = len(TEST_DATA)


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        print("Opening form at http://localhost:8080 …")
        page.goto("http://localhost:8080", wait_until="domcontentloaded")
        page.wait_for_selector(".step.is-active")

        for i, (field_type, value) in enumerate(TEST_DATA):
            step_num = i + 1
            print(f"  Step {step_num}/{TOTAL}: [{field_type}] → '{value[:40]}'")

            if field_type == "select":
                page.locator(".step.is-active .step-select").select_option(label=value)
                page.wait_for_timeout(200)
                page.locator(".step.is-active .btn-next").click()

            elif field_type == "textarea":
                page.locator(".step.is-active .step-textarea").fill(value)
                page.keyboard.press("Control+Enter")

            elif field_type == "date":
                page.locator(".step.is-active .step-input[type='date']").fill(value)
                page.wait_for_timeout(200)
                page.locator(".step.is-active .btn-next").click()

            else:
                page.locator(".step.is-active .step-input").fill(value)
                page.keyboard.press("Enter")

            # Wait for slide transition (450ms) to settle
            page.wait_for_timeout(550)

        # Verify thank-you screen
        ty = page.locator(".step--thankyou.is-active .thankyou-title")
        assert ty.is_visible(), "ERROR: Thank-you screen did not appear!"
        print("\n✓ Thank-you screen confirmed.")

        page.screenshot(path="screenshots/form_completed.png", full_page=False)
        print("✓ Screenshot saved: screenshots/form_completed.png")

        # Test restart
        page.locator(".btn-restart").click()
        page.wait_for_timeout(600)
        counter = page.locator(".step.is-active .step-counter")
        assert "1 /" in counter.text_content(), "ERROR: Restart did not return to step 1!"
        print("✓ Restart confirmed — back to step 1.\n")

        print("All checks passed!")
        input("Press Enter to close the browser…")
        browser.close()


if __name__ == "__main__":
    run()
