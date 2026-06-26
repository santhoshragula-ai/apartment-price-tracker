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
    
    print("Connecting to live RentCafe data stream...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Clean check if the flat number exists anywhere in the text block
    if "3025" in raw_text:
        print("Found Unit 3025! Extracting pricing data...")
        # Target the price directly following the unit number
        pattern = r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+)"
        match = re.search(pattern, raw_text)
        if match:
            print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
        else:
            # Fallback text slice around the unit to see how it's formatted
            start = max(0, raw_text.find("3025") - 50)
            end = min(len(raw_text), raw_text.find("3025") + 150)
            print(f"🎯 Unit 3025 Snippet: ... {raw_text[start:end]} ...")
    else:
        print("❌ Unit 3025 was not found in the raw text stream.")
        print("Printing a sample of the raw text response:")
        print(raw_text[:1000])

if __name__ == "__main__":
    check_price()
