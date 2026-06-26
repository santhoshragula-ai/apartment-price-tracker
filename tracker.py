import os
import requests
import re
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("❌ Error: SCRAPER_API_KEY environment variable is missing!")
        return

    # Use ScrapingAnt's browser rendering proxy to bypass RentCafe bot protection
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Connecting to live data stream via ScrapingAnt proxy...")
    try:
        response = requests.get(proxy_url, timeout=45)
    except Exception as e:
        print(f"❌ Proxy connection timeout: {e}")
        return
    
    if response.status_code != 200:
        print(f"❌ Proxy returned status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Safely scan the retrieved text string without risking a crash
    match = re.search(r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+|\$[\d,]+)", raw_text)
    
    if match:
        print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
    elif "3025" in raw_text:
        idx = raw_text.find("3025")
        print("Found Unit 3025 reference, but layout formatting varies.")
        print(f"Context: {raw_text[max(0, idx-50):min(len(raw_text), idx+120)]}")
    else:
        print("🔍 Unit 3025 is not explicitly visible in the returned text stream.")
        print("Attempting to parse the baseline floor plan tier pricing as fallback:")
        
        # Look for general B1 structural floor plan pricing text
        b1_match = re.search(r"B1.*?(Floorplan)?.*?(\$[\d,]+\s+-\s+\$[\d,]+|\$[\d,]+)", raw_text, re.IGNORECASE)
        if b1_match:
            print(f"🏠 General B1 Floor Plan Tier: {b1_match.group(2)}")
        else:
            print("Notice: High-level floor plan data could not be parsed from this page pull.")

if __name__ == "__main__":
    check_price()
