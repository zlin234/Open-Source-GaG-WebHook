import os
import requests
from playwright.sync_api import sync_playwright, TimeoutError

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
        page = browser.new_page()
        page.goto(url)

        try:
            page.wait_for_load_state('networkidle', timeout=30000)
        except TimeoutError:
            print("Timeout waiting for networkidle, proceeding anyway...")

        html = page.content()
        browser.close()

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)

        found_any = False
        for keyword, role_id in keyword_role_map.items():
            if keyword.lower() in html.lower():
                print(f"Keyword '{keyword}' found! Sending Discord ping to role {role_id}...")
                send_discord_ping(f"The word '{keyword}' was found on {url}!", role_id)
                found_any = True

        if not found_any:
            print("No keywords found.")

if __name__ == "__main__":
    target_url = "https://growagardenstock.com"  # Change to the URL you want to monitor
    fetch_html_and_check_words(target_url, KEYWORD_ROLE_MAP)
