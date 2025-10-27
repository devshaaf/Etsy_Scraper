import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
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
        self.pagination_container_selector = "//div[contains(@class, 'search-pagination')]"
        self.pdt_price_selector = ".//span[@class='currency-value']"
        self.rating_selector = ".//span[@class='wt-text-title-small']"
        self.review_count_selector = ".//p[@class='wt-text-body-smaller  wt-text-black']"
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.url = "https://www.etsy.com/"
        self.pageAvailable = True



    def get_element(self, parent, by, selector):
        try:
            time.sleep(1)
            element = parent.find_element(by, selector)
            return element
        except(TimeoutException,NoSuchElementException):
            print(f"Product not found {selector}")
            return "N/A"
    
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
        time.sleep(3)

        page = 1
        while self.pageAvailable:
            try:
                self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, self.pdt_list_selector))
                )

                products = self.wait.until(EC.visibility_of_all_elements_located(
                    (By.XPATH, self.pdt_card_selector)
                ))

                print(f"Found {len(products)} products in page {page}")
                for product in products:
                    time.sleep(3)
                    name = self.get_element(product, By.XPATH, self.pdt_name_selector)
                    price = self.get_element(product, By.XPATH, self.pdt_price_selector)
                    rating = self.get_element(product, By.XPATH, self.rating_selector)
                    review_count = self.get_element(product, By.XPATH, self.review_count_selector)
                    p_link = self.get_element(product, By.XPATH, self.pdt_link_selector)
                    img_link = self.get_element(product, By.XPATH, self.img_link_selector)
                    comp_name = self.get_element(product, By.XPATH, self.company_name_selector)

                    try:
                        if name != "N/A"and price != "N/A":
                            print(f"Product Name: {name.text}")
                            print(f"Price: {price.text}")
                            print(f"Rating: {rating.text}")
                            print(f"Review Count: {review_count.text}")
                            print(f"Product Link: {p_link.get_attribute('href')}")
                            print(f"Image Link: {img_link.get_attribute('src')}")
                            print(f"Company: {comp_name.text}")
                        else:
                            print("In-Complete Product")
                            continue
                    except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
                        print(f"Error in getting product details: {e}")
                        continue
                page += 1
                self.get_next_button(products)

            except:
                print("Error in scraping pages")
                self.pageAvailable = False

    def get_next_button(self, products):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        next_btn = self.driver.execute_script("""
            const container = document.querySelector('div.search-pagination');
            if (!container) return null;
            const links = container.querySelectorAll('a[data-clg-id="WtButton"] span');
            for (let span of links) {
                if (span.textContent.trim() === 'Next') {
                return span.parentElement;
                }
            }
            return null;
            """)
        try:
            print(f"Next button found: {next_btn is not None}")

            if next_btn:
                print("Next button found. Scrolling and clicking via JS...")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", next_btn)
                print("Next button clicked. Waiting for page to load...")
                if products:
                    self.wait.until(EC.staleness_of(products[0]))
                time.sleep(3)
            else:
                print("No Button found by the method.")
                self.pageAvailable = False

        except Exception as e:
            print(f"Error during pagination: {e}")
            self.pageAvailable = False


scraper = EtsyScraper()
scraper.scrape()