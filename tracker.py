import os
import requests
import re
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("❌ Error: SCRAPER_API_KEY environment variable is missing in GitHub Secrets!")
        return

    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Connecting to ScrapingAnt proxy...")
    try:
        response = requests.get(proxy_url, timeout=30)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    if response.status_code != 200:
        print(f"❌ Proxy returned status code: {response.status_code}. Your API key might be incorrect or missing.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Safely search for unit 3025 without triggering any crashes
    match = re.search(r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
    
    if match:
        print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
    elif "3025" in raw_text:
        idx = raw_text.find("3025")
        print("Found Unit 3025 reference, but the price format layout changed.")
        print(f"Context: {raw_text[max(0, idx-40):min(len(raw_text), idx+100)]}")
    else:
        print("🔍 Unit 3025 is not currently visible in the data stream.")
        print("The nested unit grid did not load. Checking for general floor plan text:")
        
        b1_match = re.search(r"B1\s+2\s+Beds.*?(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
        if b1_match:
            print(f"🏠 General B1 Price Range: {b1_match.group(1)}")
        else:
            print("No layout text found. Your API request likely returned an error page.")

if __name__ == "__main__":
    check_price()
