from .common import Vendor


class AmazonUK(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath(
            '//*[@id="availability"]/span')

        if element.text == 'Currently unavailable.':
            return 0
        else:
            return 1
