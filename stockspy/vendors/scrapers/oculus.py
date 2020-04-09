import sys
import time

from selenium.webdriver.common.by import By

from .common import Vendor


class Oculus(Vendor):
    # @Vendor.scraper
    # def get_stock(self, url):
    #     # Specifically 64gb varient.
    #     if 'Oculus Quest 64 GB is out of stock' not in self.scraper.page_source:
    #         return 1
    #     else:
    #         return 0

    @Vendor.scraper
    def get_stock(self, url):
        # Specifically 64gb varient.
        element = self.scraper.find_element_by_xpath('//*[@id="pre-orderfeatures"]/div/div/div[2]/div[2]/div/span/span[1]')

        if element.text == 'Not Available':
            print('NOT AVAILABLE')
            return 0
        else:
            print('AVAILABLE')
            return 1
