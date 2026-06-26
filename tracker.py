import os
import requests
import re
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("❌ Error: SCRAPER_API_KEY is missing!")
        return

    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Connecting to live data stream...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Safely search for unit 3025 without triggering any AttributeError crashes
    match = re.search(r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
    
    if match:
        print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
    elif "3025" in raw_text:
        idx = raw_text.find("3025")
        print("Found Unit 3025 reference, but layout format shifted.")
        print(f"Context: {raw_text[max(0, idx-40):min(len(raw_text), idx+100)]}")
    else:
        print("🔍 Unit 3025 is not currently visible in the raw page text stream.")
        print("The individual unit rows have not expanded. Pulling general B1 floor plan data as reference:")
        
        # Safe fallback pattern matching that won't break the build
        b1_match = re.search(r"B1\s+2\s+Beds.*?(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
        if b1_match:
            print(f"🏠 General B1 Price Range: {b1_match.group(1)}")
        else:
            print("Could not isolate general floor plan text.")

if __name__ == "__main__":
    check_price()
