from .common import Vendor


class Scan(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        if 'Pre Order' not in self.scraper.page_source:
            return 1
        else:
            return 0
