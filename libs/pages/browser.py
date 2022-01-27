from libs.config_reader import ConfigReader
from selenium import webdriver
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__),'..', 'config', 'default.yaml')

class Browser():

    def __init__(self):
        self.config = ConfigReader(fileName=CONFIG_FILE)
        self.baseurl = self.config.url

    def launch_chrome(self):
        '''
        :return:
        '''
        self.chrome_options = webdriver.ChromeOptions()
        if self.config.headless:
           self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
        self.browser= webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=self.chrome_options)
        self.browser.get(self.baseurl)
        return self.browser

    def refresh(self):
        self.browser.refresh()

    def navigate(self, url=''):
        self.browser.get('{}{}'.format(self.baseurl,url))

    def add_less_expensive_item(self, items: list, item_type ):
        least_expensive_item = None
        for item in items:
            name, price = item.text.splitlines()[:2]
            if item_type.lower() in name.lower():
                if not least_expensive_item:
                    least_expensive_item = item
                    continue
                current_low_price = [int(_.split()[-1]) for _ in least_expensive_item.text.splitlines()
                                                   if 'price' in _.lower()][0]
                price = int(price.split()[-1])
                if price < current_low_price:
                    least_expensive_item = item
        return least_expensive_item

    def browse_items(self,  item_type: str, first_item: str, second_item: str):
        self.browser.find_element_by_xpath(f"//*[text()='{item_type}']").click()
        all_items = self.browser.find_elements_by_xpath("//div[@class='text-center col-4']")

        first_item_to_add = self.add_less_expensive_item(all_items, first_item)
        self.browser.find_element_by_xpath(
            f"//*[text()='{first_item_to_add.text.splitlines()[0]}']//following-sibling::button").click()
        #first_item_to_add.find_element_by_xpath("//*[text()='Add']").click()

        second_item_to_add = self.add_less_expensive_item(all_items, second_item)
        self.browser.find_element_by_xpath(
            f"//*[text()='{second_item_to_add.text.splitlines()[0]}']//following-sibling::button").click()

    def proced_checkout(self):
        self.browser.find_element_by_xpath("//span[@id='cart']").click()
        # Click on Pay with Card
        self.browser.find_element_by_xpath("//*[text()='Pay with Card']").click()
        # Swtch to frame
        self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
        self.browser.find_element_by_xpath("//input[@id='email']").send_keys('test@test.com')
        # Send credit card number
        self.browser.find_element_by_xpath("//input[@id='card_number']").send_keys('4242')
        self.browser.find_element_by_xpath("//input[@id='card_number']").send_keys('4242')
        self.browser.find_element_by_xpath("//input[@id='card_number']").send_keys('4242')
        self.browser.find_element_by_xpath("//input[@id='card_number']").send_keys('4242')
        # Send expiry date
        self.browser.find_element_by_xpath("//input[@id='cc-exp']").send_keys('04')
        self.browser.find_element_by_xpath("//input[@id='cc-exp']").send_keys('25')
        # Send CVV
        self.browser.find_element_by_xpath("//input[@id='cc-csc']").send_keys('123')

        self.browser.find_element_by_xpath("//input[@id='billing-zip']").send_keys('123456')

        self.browser.find_element_by_xpath("//button[@id='submitButton']").click()

