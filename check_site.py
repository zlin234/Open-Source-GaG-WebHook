import os
import requests
from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Map each keyword to the Discord role ID to ping
KEYWORD_ROLE_MAP = {
    "Mushroom": "1377186156982046791",
    "Grape": "1377186235335835718",
    "Cacao": "1377186318999752744",
    "Bamboo": "1378271980255449149",
    "Apple": "1378273610103521351",
    "Beanstalk": "1377186479389933568",
    "Mango": "1377213063752581151",
    "Dragon": "1377213106345873428",
    # add more keywords and role IDs as needed
}

def send_discord_ping(message: str, role_id: str):
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL not set in environment variable.")
        return

    mention = f"<@&{role_id}>"
    data = {"content": f"{mention} {message}"}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"Discord notification sent successfully for role {role_id}.")
    else:
        print(f"Failed to send Discord notification: {response.status_code} - {response.text}")

def fetch_html_and_check_words(url: str, keyword_role_map: dict):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Create fresh context with a realistic user agent
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.reload(wait_until="networkidle")
            page.wait_for_timeout(5000)  # wait extra for dynamic content
        except TimeoutError:
            print("Timeout waiting for networkidle, proceeding anyway...")

        html = page.content()
        browser.close()

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"[{now}] Fetched HTML snippet:\n{html[:500]}...\n")

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(f"<!-- Fetched at {now} -->\n")
            f.write(html)

        found_any = False
        for keyword, role_id in keyword_role_map.items():
            if keyword.lower() in html.lower():
                print(f"Keyword '{keyword}' found! Sending Discord ping to role {role_id}...")
                send_discord_ping(f"The word '{keyword}' was found on {url}!", role_id)
                found_any = True

        if not found_any:
            print("No keywords found.")
