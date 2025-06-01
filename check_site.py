import os
import requests
import random
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

KEYWORD_ROLE_MAP = {
    "Mushroom": "1377186156982046791",
    "Grape": "1377186235335835718",
    "Cacao": "1377186318999752744",
    "Bamboo": "1378271980255449149",
    "Apple": "1378273610103521351",
    "Beanstalk": "1377186479389933568",
    "Mango": "1377213063752581151",
    "Dragon": "1377213106345873428",
    "Carrot": "1377597478383255576",
    "Daffodil": "1377597478383255576",
}

def send_discord_ping(message: str, role_id: str):
    # ... existing implementation ...

def fetch_html_and_check_words(url: str, keyword_role_map: dict):
    with sync_playwright() as p:
        # Launch browser with anti-detection measures
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox"
            ]
        )
        
        # Create new context with cache disabled
        context = browser.new_context(
            bypass_csp=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            extra_http_headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
        page = context.new_page()
        
        # Add cache-busting parameter
        separator = "?" if "?" not in url else "&"
        navigated_url = f"{url}{separator}cb={random.randint(100000,999999)}"
        
        try:
            # Load page with multiple wait strategies
            page.goto(
                navigated_url,
                timeout=90000,
                wait_until="commit"
            )
            
            # Wait for critical elements to load
            page.wait_for_selector("body", state="attached", timeout=30000)
            
            # Wait for network stability
            page.wait_for_load_state("networkidle", timeout=30000)
            
            # Additional wait for dynamic content
            time.sleep(3)
            
            # Take screenshot for debugging
            page.screenshot(path="screenshot.png", full_page=True)
            
        except PlaywrightTimeoutError:
            print("Timeout occurred - using current content")
            page.screenshot(path="timeout_screenshot.png", full_page=True)
        except Exception as e:
            print(f"Navigation error: {e}")
            context.close()
            browser.close()
            return
            
        html = page.content()
        
        # Close browser
        context.close()
        browser.close()

        # Save HTML for debugging
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Check for keywords
        html_lower = html.lower()
        found_any = False
        for keyword, role_id in keyword_role_map.items():
            if keyword.lower() in html_lower:
                print(f"Found keyword: {keyword}")
                send_discord_ping(f"Keyword '{keyword}' detected on {url}!", role_id)
                found_any = True

        if not found_any:
            print("No keywords detected")

if __name__ == "__main__":
    target_url = "https://growagardenstock.com"
    fetch_html_and_check_words(target_url, KEYWORD_ROLE_MAP)
