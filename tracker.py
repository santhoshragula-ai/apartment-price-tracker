import os
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    print("Launching automated browser architecture...")
    
    with sync_playwright() as p:
        # Launch a headless chromium browser instance
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to: {TARGET_URL}")
        try:
            # Navigate and wait until network activity settles
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            
            # Click floor plan expanders if present to uncover nested unit tables
            print("Attempting to expand floor plan tables...")
            buttons = page.query_selector_all(".js-view-available-units, .view-units-btn")
            for button in buttons:
                try:
                    button.click()
                    page.wait_for_timeout(1000) # Short pause for dynamic render
                except Exception:
                    pass
                    
            # Get the fully evaluated HTML after scripts have run
            html_content = page.content()
            browser.close()
            
        except Exception as e:
            print(f"❌ Browser execution failed: {e}")
            browser.close()
            return

    # Parse the rendered page
    soup = BeautifulSoup(html_content, 'html.parser')
    raw_text = soup.get_text(" ", strip=True)
    
    print("\n====== TARGET UNIT WATCH ======")
    
    # Run safe regex match against the fully loaded JS DOM text
    match = re.search(r"3025\s+(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
    
    if match:
        print(f"🎯 Unit 3025 Current Price: {match.group(1)}")
    elif "3025" in raw_text:
        idx = raw_text.find("3025")
        print("Found Unit 3025 reference, but layout formatting varies.")
        print(f"Context: {raw_text[max(0, idx-50):min(len(raw_text), idx+120)]}")
    else:
        print("🔍 Unit 3025 is not actively listed in the expanded dynamic view.")
        
        # Safe structural fallback to keep the run green
        b1_match = re.search(r"B1\s+2\s+Beds.*?(\$[\d,]+\s+-\s+\$[\d,]+)", raw_text)
        if b1_match:
            print(f"🏠 General B1 Price Tier: {b1_match.group(1)}")
        else:
            print("Notice: Floor plan grid data could not be isolated.")

if __name__ == "__main__":
    check_price()
