from .common import Vendor


class Argos(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        return 1
