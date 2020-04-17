from .common import Vendor


class Very(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath('//*[@id="E3921-stockMessaging"]/span[1]')

        if element.text == 'Out of stock':
            return 0
        else:
            return 1
