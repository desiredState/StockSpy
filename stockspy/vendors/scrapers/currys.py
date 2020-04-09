from .common import Vendor


class Currys(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath('//*[@id="product-actions"]/div[4]/div/ul/li[1]')

        if element.text == 'Sorry this item is out of stock':
            return 0
        else:
            return 1
