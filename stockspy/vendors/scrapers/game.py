from .common import Vendor


class Game(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath('//*[@id="pdp"]/aside/div[1]/div[1]/div[2]')

        if 'out of stock' in element.text:
            return 0
        else:
            return 1
