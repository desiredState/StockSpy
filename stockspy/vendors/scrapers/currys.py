from .common import Vendor


class Currys(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        if 'out of stock' not in self.scraper.page_source:
            return 1
        else:
            return 0
