from .common import Vendor


class Argos(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        if 'Not available' not in self.scraper.page_source:
            return 1
        else:
            return 0
