from .common import Vendor


class Scan(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath(
            '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/span[2]')

        if 'Item due on' in element.text:
            return 0
        else:
            return 1
