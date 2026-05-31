"""
Take a full-page screenshot of any URL and save it to disk.

Usage: python3 scripts/screenshot.py <url> [output.png]
"""
import sys
from playwright.sync_api import sync_playwright

def screenshot(url: str, output: str = "screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=output, full_page=True)
        browser.close()
    print(f"Saved: {output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/screenshot.py <url> [output.png]")
        sys.exit(1)
    url = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
    screenshot(url, out)
