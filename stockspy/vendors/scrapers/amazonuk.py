from .common import Vendor


class AmazonUK(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        if 'Buy new' in self.scraper.page_source:
            return 1
        else:
            return 0
