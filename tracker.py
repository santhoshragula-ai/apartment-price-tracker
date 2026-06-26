import os
import requests
import re
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Connecting to live data stream...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Target the exact sequence for unit 3025 found in your previous working log
    pattern = r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+)"
    match = re.search(pattern, raw_text)
    
    if match:
        print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
    else:
        # Flexible context fallback if spacing inside the single-line string shifts
        fallback_pattern = r"(3025.*?Apply now)"
        fallback_match = re.search(fallback_pattern, raw_text)
        if fallback_match:
            print(f"🎯 Unit 3025 Context: {fallback_match.group(1)}")
        else:
            print("❌ Unit 3025 was not found in this data pull. Checking raw sample:")
            print(raw_text[:500])

if __name__ == "__main__":
    check_price()
