import os
import requests
import random
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
    # ... other keywords ...
}

def send_discord_ping(message: str, role_id: str):
    # ... unchanged code ...

def fetch_html_and_check_words(url: str, keyword_role_map: dict):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Create new context with disabled caching
        context = browser.new_context(
            bypass_csp=True,
            ignore_https_errors=True,
            # Disable caching
            no_viewport=True,
            java_script_enabled=True
        )
        
        page = context.new_page()
        
        # Add cache-busting parameter to URL
        cache_buster = random.randint(100000, 999999)
        separator = "?" if "?" not in url else "&"
        navigated_url = f"{url}{separator}cache_buster={cache_buster}"
        
        try:
            # Load page with aggressive cache prevention
            page.goto(
                navigated_url,
                timeout=60000,
                wait_until="domcontentloaded"
            )
            
            # Wait for dynamic content (adjust selector as needed)
            page.wait_for_selector("body", state="attached", timeout=30000)
            
            # Additional wait for network stability
            page.wait_for_timeout(2000)  # Allow 2 seconds for JS execution
            
        except PlaywrightTimeoutError:
            print("Timeout during page loading, using current content")
        except Exception as e:
            print(f"Error loading page: {e}")
            context.close()
            browser.close()
            return
            
        # Get final rendered HTML
        html = page.content()
        
        context.close()
        browser.close()

        # ... keyword checking logic ...

if __name__ == "__main__":
    target_url = "https://growagardenstock.com"
    fetch_html_and_check_words(target_url, KEYWORD_ROLE_MAP)
