import time
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class EtsyScraper:
    def __init__(self):
        self.search_input_selector = "//input[@data-id='search-query']"
        self.search_btn_selector = "//button[@data-id='gnav-search-submit-button']"
        self.pdt_list_selector = "//ul[@class='wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container']"
        self.pdt_card_selector = "//li[@class='wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 ']"
        self.img_link_selector = ".//img[@data-clg-id='WtImage']"
        self.pdt_link_selector = ".//a[contains(@class, 'listing-link')]"
        self.pdt_name_selector = ".//h3[contains(@class, 'wt-text-body-small')]"
        self.company_name_selector = ".//span[contains(@class,'clickable-shop-name')]"
        self.next_btn_selector = "//a[.//span[normalize-space(text())='Next']]"
        self.pdt_price_selector = ".//span[@class='currency-value']"
        self.rating_selector = ".//span[@class='wt-text-title-small']"
        self.review_count_selector = ".//p[@class='wt-text-body-smaller  wt-text-black']"
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://www.etsy.com/"

    def scrape(self):
        self.driver.get(self.url)
        search_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.search_input_selector)
        ))
        search_input.send_keys("handmade mug")
        search_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.search_btn_selector)
        ))
        search_btn.click()
        time.sleep(2)


        while True:
            time.sleep(2)
            try:
                products = self.driver.find_elements(By.XPATH, self.pdt_card_selector)
                print(f"{len(products)} products found")
            except:
                print("No products found")
                return

            time.sleep(5)

            for product in products:
                product_name = product.find_element(By.XPATH, self.pdt_name_selector)
                product_price = product.find_element(By.XPATH, self.pdt_price_selector)
                try:
                    product_rating = product.find_element(By.XPATH, self.rating_selector)
                    product_reviews = product.find_element(By.XPATH, self.review_count_selector)
                    product_link = product.find_element(By.XPATH, self.pdt_link_selector)
                except NoSuchElementException:
                    product_rating = None
                    product_reviews = None
                    product_link = None
                image_link = product.find_element(By.XPATH, self.img_link_selector)
                company_name = product.find_element(By.XPATH, self.company_name_selector)

                print(f"name: {product_name.text}")
                print(f"price: {product_price.text}")
                if product_rating and product_reviews and product_link:
                    print(f"rating: {product_rating.text}")
                    print(f"r_count: {product_reviews.text}")
                    print(f"p_link: {product_link.get_attribute('href')}")
                else:
                    print(f"rating: {product_rating}")
                    print(f"r_count: {product_reviews}")
                    print(f"p_link: {product_link}")
                print(f"img_link: {image_link.get_attribute('src')}")
                print(f"comp_name: {company_name.text}")

            try:
                next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.next_btn_selector)))
                print("Clicked Next Button")
                next_btn.click()
            except (TimeoutException, ElementNotInteractableException):
                print("No more pages to scrape")
                break




scraper = EtsyScraper()
scraper.scrape()


