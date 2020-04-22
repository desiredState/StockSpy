from .common import Vendor


class JohnLewis(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath(
            '//*[@id="button--add-to-basket-out-of-stock"]')

        if element.text == 'Currently unavailable':
            return 0
        else:
            return 1
