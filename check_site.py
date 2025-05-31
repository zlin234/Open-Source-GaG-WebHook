from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')  # Required in GitHub Actions
options.add_argument('--disable-dev-shm-usage')  # Prevent crashes in CI

driver = webdriver.Chrome(options=options)

driver.get('https://example.com')
html = driver.page_source

with open('rendered_output.html', 'w', encoding='utf-8') as f:
    f.write(html)

driver.quit()
