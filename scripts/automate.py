"""
Example browser automation: navigate to Hacker News and grab top story titles.
Demonstrates navigation, waiting, locator selection, and scraping.

Usage: python3 scripts/automate.py
"""
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False so you can watch
        page = browser.new_page()

        print("Navigating to Hacker News...")
        page.goto("https://news.ycombinator.com")
        page.wait_for_load_state("networkidle")

        # Grab top story titles
        titles = page.locator(".titleline > a").all_text_contents()
        print(f"\nTop {len(titles)} stories:")
        for i, title in enumerate(titles[:10], 1):
            print(f"  {i}. {title}")

        # Take a screenshot before closing
        page.screenshot(path="screenshots/hn.png")
        print("\nScreenshot saved: screenshots/hn.png")

        input("\nPress Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    run()
