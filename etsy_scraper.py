from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

search_input_selector = "//input[@data-id='search-query']"
search_btn_selector = "//button[@data-id='gnav-search-submit-button']"
pdt_list_selector = "//ul[@class='wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container']"
pdt_card_selector = "//li[@class='wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 ']"
img_link_selector = ".//img[@data-clg-id='WtImage']"
pdt_link_selector = ".//a[contains(@class, 'listing-link')]"
pdt_name_selector = ".//h3[contains(@class, 'wt-text-body-small')]"
company_name_selector = ".//span[contains(@class,'clickable-shop-name')]"
next_btn_selector = "//a[@class='wt-btn wt-action-group__item wt-btn--small wt-btn--icon']"
pdt_price_selector = ".//span[@class='currency-value']"
rating_selector = ".//span[@class='wt-text-title-small']"
review_count_selector = ".//p[@class='wt-text-body-smaller  wt-text-black']"

url = "https://www.etsy.com/"
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get(url)

try:
    search_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, search_input_selector)
    ))
    search_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, search_btn_selector)
    ))
    print(search_input)
    search_input.send_keys("handmade mug")
    search_btn.click()

    next_btn = driver.find_element(By.XPATH, next_btn_selector)

    if wait.until(EC.visibility_of_element_located((By.XPATH, pdt_list_selector))):
        product_cards = driver.find_elements(By.XPATH, pdt_card_selector)
        # product_card.click()
        print(f'Total {len(product_cards)} products found in this page')
        for product_card in product_cards:
            try:
                company_name = product_card.find_element(By.XPATH, company_name_selector)
                product_name = product_card.find_element(By.XPATH, pdt_name_selector)
                product_link = product_card.find_element(By.XPATH, pdt_link_selector)
                img_link = product_card.find_element(By.XPATH, img_link_selector)
                product_price = product_card.find_element(By.XPATH, pdt_price_selector)
                review = product_card.find_element(By.XPATH, rating_selector)
                review_count = product_card.find_element(By.XPATH, review_count_selector)
                print(f'Product name: {product_name.text}')
                print(f'Company name: {company_name.text}')
                print(f'Product link: {product_link.get_attribute('href')}')
                print(f'Image link: {img_link.get_attribute('src')}')
                print(f'Product price: {product_price.text}')
                print(f'Rating: {review.text}')
                print(f'Review count: {review_count.text}')
            except Exception as e:
                print("Error in finding product elements")
    else:
        print("products list not found")

except Exception as e:
    print(f"Error: {e}")
finally:
    time.sleep(10)
    driver.quit()
