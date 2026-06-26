import os
import requests
import re
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is missing!")
        return

    # Instructs the browser to look for the floor plan grid button and click it to expose individual units
    js_click_script = "document.querySelectorAll('.js-view-available-units, .view-units-btn').forEach(btn => btn.click());"
    
    import urllib.parse
    encoded_js = urllib.parse.quote(js_click_script)
    
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true&js_snippet={encoded_js}"
    
    print("Connecting to live data stream and expanding unit grids...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Target unit 3025 safely
    match = re.search(r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
    
    if match:
        print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
    elif "3025" in raw_text:
        idx = raw_text.find("3025")
        print("Found Unit 3025 reference! Context:")
        print(raw_text[max(0, idx-40):min(len(raw_text), idx+120)])
    else:
        print("🔍 Unit 3025 is hidden or unexpanded in this pull.")
        print("Checking for general B1 floor plan data:")
        b1_match = re.search(r"B1\s+2\s+Beds.*?(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
        if b1_match:
            print(f"🏠 General B1 Floor Plan Range: {b1_match.group(1)}")

if __name__ == "__main__":
    check_price()
