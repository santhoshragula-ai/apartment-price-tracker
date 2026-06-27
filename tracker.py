import os
import re
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"
# Changed threshold to 1500 per your request
BASE_PRICE_THRESHOLD = 1500

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("❌ Error: SCRAPER_API_KEY missing!")
        return

    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Connecting to live data stream via ScrapingAnt proxy...")
    try:
        response = requests.get(proxy_url, timeout=45)
    except Exception as e:
        print(f"❌ Proxy connection timeout: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Extract the numerical range out of the text string
    match = re.search(r"3025\s+\$(\d[\d,]+)", raw_text)
    
    if match:
        current_low_price = int(match.group(1).replace(',', ''))
        print(f"🎯 Unit 3025 Current Starting Price: ${current_low_price:,}")
        
        # Trigger email generation logic only if price dips below $1500
        if current_low_price < BASE_PRICE_THRESHOLD:
            print(f"🚨 Price drop detected below ${BASE_PRICE_THRESHOLD}! Creating email trigger flag...")
            with open("send_email.txt", "w") as f:
                f.write(f"Price dropped to ${current_low_price}")
        else:
            print(f"No drop detected. Current price (${current_low_price:,}) is higher than threshold (${BASE_PRICE_THRESHOLD:,})")
            
    elif "3025" in raw_text:
        print("Found Unit 3025 reference, but price structure layout shifted.")
    else:
        print("🔍 Unit 3025 is not explicitly visible in the returned text stream right now.")

if __name__ == "__main__":
    check_price()
