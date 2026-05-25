from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
import re  

driver = webdriver.Chrome()  
wait = WebDriverWait(driver, 15)  

# FIX: remove empty lines
codes = [c.strip() for c in open("codes.txt").read().splitlines() if c.strip()]

results = []  # store results

# =========================  
# COOKIE HANDLER (COOKIEBOT)  
# =========================  
def handle_cookies():  
    try:  
        iframes = driver.find_elements(By.TAG_NAME, "iframe")  
        for iframe in iframes:  
            driver.switch_to.frame(iframe)  
            try:  
                btn = driver.find_element(By.XPATH, "//button[contains(., 'Allow all cookies')]")  
                btn.click()  
                print("Cookies accepted (iframe)")  
                driver.switch_to.default_content()  
                return  
            except:  
                driver.switch_to.default_content()  

        btn = driver.find_element(By.XPATH, "//button[contains(., 'Allow all cookies')]")  
        btn.click()  
        print("Cookies accepted (direct)")  

    except:  
        print("No cookie popup found")  

# =========================  
# MAIN LOOP  
# =========================  
for i, code in enumerate(codes, 1):  
    print(f"\n[{i}/{len(codes)}] Checking {code}...")  

    url = f"https://www.booker.co.uk/products/product-search?keywords={code}"  
    driver.get(url)  

    handle_cookies()  

    try:  
        wait.until(  
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'£')]"))  
        )  

        price_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'£')]")  

        price = "NOT_FOUND"  

        for el in price_elements:  
            text = el.text.strip()  

            if any(x in text.lower() for x in ["was", "save", "rrp", "por", "pm", "vat"]):  
                continue  

            clean_text = text.replace(" ", "")  
            match = re.search(r"£\d+(\.\d{2})?", clean_text)  

            if match:  
                price = match.group()  
                break  

    except Exception as e:  
        print(f"[ERROR] {code}: {e}")  
        price = "NOT_FOUND"  

    print("→", price)  
    results.append((code, price))  # store result

driver.quit()

# =========================
# WRITE OUTPUT FILE
# =========================

with open("new_prices.txt", "w") as f:
    for code, price in results:
        f.write(f"{code}\t{price}\n")

print("\nSaved to new_prices.txt")
