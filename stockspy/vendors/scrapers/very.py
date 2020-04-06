from .common import Vendor


class Very(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        if 'Out of stock' not in self.scraper.page_source:
            return 1
        else:
            return 0
