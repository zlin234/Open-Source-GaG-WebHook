import requests
from bs4 import BeautifulSoup
import os

# Configuration
url = "https://growagardenstock.com"  # Your target site
output_file = "downloaded_page.html"
keywords = ["example", "domain", "test"]
webhook_url = os.getenv("DISCORD_WEBHOOK")  # Discord webhook from secret

# Fetch HTML
try:
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
except requests.RequestException as e:
    print(f"Failed to fetch HTML: {e}")
    exit(1)

# Overwrite HTML file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

# Search for keywords
soup = BeautifulSoup(html_content, "html.parser")
text = soup.get_text().lower()

found_keywords = [kw for kw in keywords if kw.lower() in text]

# Send webhook if any keywords are found
if found_keywords and webhook_url:
    mentions = "<@&ROLE_ID_1> <@&ROLE_ID_2>"  # Replace with actual Discord role IDs
    message = {
        "content": f"{mentions}\nKeyword(s) found on {url}: {', '.join(found_keywords)}"
    }
    try:
        r = requests.post(webhook_url, json=message)
        r.raise_for_status()
        print("Webhook sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send webhook: {e}")
else:
    print("No keywords found or webhook URL missing.")
