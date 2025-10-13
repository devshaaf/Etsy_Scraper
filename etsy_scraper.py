import time
from selenium import webdriver
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
        self.next_btn_selector = "//*[@id='content']/div/div[1]/div/div[4]/div[9]/div[2]/div[8]/div/div/div/div[2]/nav/div/div[9]/a"
        self.pdt_price_selector = ".//span[@class='currency-value']"
        self.rating_selector = ".//span[@class='wt-text-title-small']"
        self.review_count_selector = ".//p[@class='wt-text-body-smaller  wt-text-black']"
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://www.etsy.com/"

    def scrape_products(self):
        self.driver.get(self.url)
        search_input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.search_input_selector)
        ))
        search_input.send_keys("Bags")
        search_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.search_btn_selector)
        ))
        search_btn.click()
        time.sleep(2)
        page=1
        while self.wait.until(EC.visibility_of_element_located((By.XPATH, self.next_btn_selector))):
            next_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, self.next_btn_selector)
            ))

            if self.wait.until(EC.presence_of_element_located((By.XPATH, self.pdt_list_selector))):
                products = self.driver.find_elements(By.XPATH, self.pdt_card_selector)
                for product in products:
                    print(f"{len(products)} products found in page {page}")
                    product_name = product.find_element(By.XPATH, self.pdt_name_selector).text
                    product_price = product.find_element(By.XPATH, self.pdt_price_selector).text
                    rating = product.find_element(By.XPATH, self.rating_selector).text or 'N/A'
                    review_count = product.find_element(By.XPATH, self.review_count_selector).text or 'N/A'
                    product_link = product.find_element(By.XPATH, self.pdt_link_selector).get_attribute('href') or 'N/A'
                    image_link = product.find_element(By.XPATH, self.img_link_selector).get_attribute('src') or 'N/A'
                    company_name = product.find_element(By.XPATH, self.company_name_selector).text
                    print(f'product name: {product_name}')
                    print(f'product price: {product_price}')
                    print(f'product rating: {rating}')
                    print(f'product review count: {review_count}')
                    print(f'product link: {product_link}')
                    print(f'product image link: {image_link}')
                    print(f'Company name: {company_name}')
            print("Clicked Next Button")
            next_btn.click()
            page+=1




scraper = EtsyScraper()
scraper.scrape_products()


