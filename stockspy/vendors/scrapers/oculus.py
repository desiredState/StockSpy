from .common import Vendor


class Oculus(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        # Specifically 60gb varient.
        if '<span class="_7w4j"><span class="_7w4l">Not Available</span><sup>*</sup><span class="_7w4k"></span><span class="_7w54"><span class="_7w55">64</span><span class="_7w56">GB</span><sup class="_7w57">1</sup></span></span>' not in self.scraper.page_source:
            return 1
        else:
            return 0
