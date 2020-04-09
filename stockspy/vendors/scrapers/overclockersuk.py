from .common import Vendor


class OverclockersUK(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath('//*[@id="buybox"]/span/p')

        if element.text == 'Out of stock':
            return 0
        else:
            return 1
