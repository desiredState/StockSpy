from .common import Vendor


class Oculus(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        # Specifically 64gb varient.
        if 'Oculus Quest 64 GB is out of stock' not in self.scraper.page_source:
            return 1
        else:
            return 0
