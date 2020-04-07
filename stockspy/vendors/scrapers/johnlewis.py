from .common import Vendor


class JohnLewis(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        if 'Currently unavailable' not in self.scraper.page_source:
            return 1
        else:
            return 0
