"""End-to-end QA agent for the onboarding form.

The agent starts an isolated local server (unless QA_BASE_URL is set), opens the
form in Chromium, and runs the high-value checks from docs/TEST_CASES.md.

Usage:
    python3 scripts/qa_agent.py
    python3 scripts/qa_agent.py --headed
    QA_BASE_URL=http://localhost:8080 python3 scripts/qa_agent.py
"""

from __future__ import annotations

import functools
import os
import sys
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import Browser, Page, sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HEADLESS = "--headed" not in sys.argv
if not HEADLESS:
    sys.argv.remove("--headed")


class QuietStaticHandler(SimpleHTTPRequestHandler):
    """Keep the QA output focused on case results instead of HTTP access logs."""

    def log_message(self, format: str, *args: object) -> None:
        pass


class LocalFormServer:
    """Serve the repository from an available loopback port for the test run."""

    def __enter__(self) -> str:
        handler = functools.partial(QuietStaticHandler, directory=str(PROJECT_ROOT))
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address
        return f"http://{host}:{port}"

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


class OnboardingFormQA(unittest.TestCase):
    """A browser-level regression suite organized by the documented test cases."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.local_server = None
        cls.base_url = os.getenv("QA_BASE_URL")
        if not cls.base_url:
            cls.local_server = LocalFormServer()
            cls.base_url = cls.local_server.__enter__()

        cls.playwright = sync_playwright().start()
        cls.browser: Browser = cls.playwright.chromium.launch(headless=HEADLESS)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.playwright.stop()
        if cls.local_server:
            cls.local_server.__exit__(None, None, None)

    def setUp(self) -> None:
        self.page: Page = self.browser.new_page(viewport={"width": 1280, "height": 900})
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        self.page.locator(".step.is-active").wait_for()

    def tearDown(self) -> None:
        self.page.close()

    def active_step(self, number: int) -> None:
        """Assert that exactly the requested numbered form step is active."""
        active = self.page.locator(".step.is-active")
        self.assertEqual(active.locator(".step-counter").inner_text(), f"{number} / 12")

    def advance_with_text(self, value: str) -> None:
        field = self.page.locator(".step.is-active .step-input")
        field.fill(value)
        field.press("Enter")
        self.page.wait_for_timeout(150)

    def advance_with_select(self, label: str) -> None:
        self.page.locator(".step.is-active .step-select").select_option(label=label)
        self.page.locator(".step.is-active .btn-next").click()
        self.page.wait_for_timeout(150)

    def advance_with_textarea(self, value: str) -> None:
        field = self.page.locator(".step.is-active .step-textarea")
        field.fill(value)
        field.press("Control+Enter")
        self.page.wait_for_timeout(150)

    def advance_empty(self, key: str = "Enter") -> None:
        self.page.locator(".step.is-active .step-input").press(key)
        self.page.wait_for_timeout(150)

    def complete_questions(self) -> None:
        """Complete required fields and deliberately skip all optional fields."""
        self.advance_with_text("Ada")                  # q1, required
        self.advance_with_text("Lovelace")             # q2, required
        self.advance_empty()                             # q3, optional phone
        self.advance_with_text("Analytical Engines")    # q4, required
        self.advance_with_text("Engineer")              # q5, required
        self.advance_with_select("Technology / SaaS")   # q6, required
        self.advance_with_select("2–10")                # q7, required
        self.advance_empty()                             # q8, optional
        self.advance_with_textarea("Turning interested visitors into customers.")
        self.advance_with_textarea("Grow recurring revenue sustainably.")
        self.page.locator(".step.is-active .btn-next").click()  # q11, optional date
        self.page.wait_for_timeout(150)
        self.advance_empty("Control+Enter")             # q12, optional textarea

    def test_tc_01_initial_render_and_accessible_labels(self) -> None:
        """TC-01/02/26-30: initial UI, progress, and optional indicators."""
        self.active_step(1)
        self.assertEqual(self.page.locator("label[for='q1']").inner_text(), "What's your first name?")
        self.assertEqual(self.page.locator(".step-optional").count(), 4)
        progress = self.page.locator("#progress-bar-fill").evaluate("el => el.style.width")
        self.assertAlmostEqual(float(progress.rstrip("%")), 100 / 14, places=4)

    def test_tc_17_required_fields_block_navigation_then_recover(self) -> None:
        """TC-17/19: required validation shows an error and valid input clears it."""
        self.page.locator(".step.is-active .btn-next").click()
        error = self.page.locator(".step.is-active .step-error")
        self.assertEqual(error.inner_text(), "This field is required — please fill it in.")
        self.active_step(1)

        self.advance_with_text("Ada")
        self.active_step(2)
        self.assertEqual(error.inner_text(), "")

    def test_tc_20_to_22_optional_phone_and_phone_validation(self) -> None:
        """TC-20-22: optional phone can be skipped, but supplied values are validated."""
        self.advance_with_text("Ada")
        self.advance_with_text("Lovelace")
        self.active_step(3)

        self.advance_with_text("123")
        self.assertIn("valid phone number", self.page.locator(".step.is-active .step-error").inner_text())
        self.active_step(3)

        self.advance_with_text("+1 (555) 123-4567")
        self.active_step(4)

    def test_tc_13_to_16_keyboard_and_select_navigation(self) -> None:
        """TC-13-16/31-35: textarea shortcuts and required select behavior."""
        self.advance_with_text("Ada")
        self.advance_with_text("Lovelace")
        self.advance_empty()
        self.advance_with_text("Analytical Engines")
        self.advance_with_text("Engineer")
        self.active_step(6)

        select = self.page.locator(".step.is-active .step-select")
        self.assertEqual(select.locator("option").count(), 8)
        self.page.locator(".step.is-active .btn-next").click()
        self.assertIn("required", self.page.locator(".step.is-active .step-error").inner_text())
        self.advance_with_select("Technology / SaaS")
        self.advance_with_select("2–10")
        self.advance_empty()
        self.active_step(9)

        textarea = self.page.locator(".step.is-active .step-textarea")
        textarea.fill("First line")
        self.advance_empty()
        self.assertEqual(textarea.input_value(), "First line\n")
        self.active_step(9)
        self.page.keyboard.press("Control+Enter")
        self.active_step(10)

    def test_tc_64_submission_review_can_edit_answers_before_confirming(self) -> None:
        """TC-64-66: review shows all answers, supports editing, then confirms."""
        self.complete_questions()
        review = self.page.locator(".step--review.is-active")
        self.assertTrue(review.is_visible())
        self.assertEqual(review.locator(".review-item").count(), 12)
        self.assertEqual(review.locator(".review-answer").nth(0).inner_text(), "Ada")
        self.assertEqual(review.locator(".review-answer").nth(2).inner_text(), "Not provided")
        progress = self.page.locator("#progress-bar-fill").evaluate("el => el.style.width")
        self.assertLess(float(progress.rstrip("%")), 100)

        review.locator(".review-edit").nth(0).click()
        self.active_step(1)
        self.assertEqual(self.page.locator("#q1").input_value(), "Ada")

        # Existing answers remain available while navigating back to review.
        self.advance_empty()
        self.advance_empty()
        self.advance_empty()
        self.advance_empty()
        self.advance_empty()
        self.page.locator(".step.is-active .btn-next").click()
        self.page.wait_for_timeout(150)
        self.page.locator(".step.is-active .btn-next").click()
        self.page.wait_for_timeout(150)
        self.advance_empty()
        self.advance_empty("Control+Enter")
        self.advance_empty("Control+Enter")
        self.page.locator(".step.is-active .btn-next").click()
        self.page.wait_for_timeout(150)
        self.advance_empty("Control+Enter")
        self.assertTrue(self.page.locator(".step--review.is-active").is_visible())
        self.page.locator(".btn-submit").click()
        self.assertTrue(self.page.locator(".step--thankyou.is-active").is_visible())

    def test_tc_07_to_09_full_submission_progress_and_restart(self) -> None:
        """TC-07-09/24-25: full journey, completion state, and reset behavior."""
        self.complete_questions()
        self.page.locator(".btn-submit").click()
        thank_you = self.page.locator(".step--thankyou.is-active")
        self.assertTrue(thank_you.locator(".thankyou-title").is_visible())
        self.assertEqual(thank_you.locator(".thankyou-title").inner_text(), "You're all set!")
        self.assertEqual(self.page.locator("#progress-bar-fill").evaluate("el => el.style.width"), "100%")

        self.page.locator(".btn-restart").click()
        self.active_step(1)
        self.assertEqual(self.page.locator("#q1").input_value(), "")
        self.assertEqual(self.page.locator("#q6").input_value(), "")

    def test_tc_38_mobile_next_button_uses_card_width(self) -> None:
        """TC-38: the primary action is full width at the mobile breakpoint."""
        self.page.set_viewport_size({"width": 390, "height": 844})
        button_box = self.page.locator(".step.is-active .btn-next").bounding_box()
        content_width = self.page.locator(".step.is-active").evaluate(
            """el => {
                const style = getComputedStyle(el);
                return el.clientWidth
                    - parseFloat(style.paddingLeft)
                    - parseFloat(style.paddingRight);
            }"""
        )
        self.assertIsNotNone(button_box)
        self.assertAlmostEqual(button_box["width"], content_width, delta=1)


if __name__ == "__main__":
    print(f"QA agent target: {os.getenv('QA_BASE_URL', 'isolated local server')}")
    print(f"Browser mode: {'headless' if HEADLESS else 'headed'}")
    unittest.main(verbosity=2)
