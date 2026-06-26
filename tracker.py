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
    
    print("Connecting to La Costa pricing data...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== REAL-TIME 2-BEDROOM PRICES ======")
    
    # This regular expression locks onto the models (B1, B2, B3, B4) and extracts their specific details
    models = ["B1", "B2", "B3", "B4"]
    for model in models:
        pattern = rf"({model}\s+2\s+Beds\s+/\s+2\s+Baths\s+/\s+[\d,]+\s+Sqft\s+\$[\d,]+\s+-\s+\$[\d,]+)"
        match = re.search(pattern, raw_text)
        if match:
            print(f"🏠 Model {match.group(1)}")
        else:
            # Fallback: simpler match if layout shifts slightly
            fallback_pattern = rf"({model}\s+2\s+Beds.*?\$[\d,]+\s+-\s+\$[\d,]+)"
            fallback_match = re.search(fallback_pattern, raw_text)
            if fallback_match:
                print(f"🏠 Model {fallback_match.group(1)}")

if __name__ == "__main__":
    check_price()
