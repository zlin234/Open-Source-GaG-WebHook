import requests
from playwright.sync_api import sync_playwright

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1377588810522562560/SFFtoKG5kfKrV1rOuRI9NK_CKV8-UQ5QA7TJ9k9oUKmKIj95gsTot6X-8aID2KNosKog"

def send_discord_ping(message: str):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Discord notification sent successfully.")
    else:
        print(f"Failed to send Discord notification: {response.status_code} - {response.text}")

def fetch_html_and_check_word(url: str, keyword: str = "carrot"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        html = page.content()
        browser.close()

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)

        if keyword.lower() in html.lower():
            print(f"Keyword '{keyword}' found! Sending Discord ping...")
            send_discord_ping(f":carrot: The word '{keyword}' was found on {url}!")
        else:
            print(f"Keyword '{keyword}' not found.")

if __name__ == "__main__":
    target_url = "https://growagardenstock.com"  # Change this URL
    fetch_html_and_check_word(target_url)
