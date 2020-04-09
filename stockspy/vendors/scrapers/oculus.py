from .common import Vendor


class Oculus(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        # Specifically 64gb varient.
        element = self.scraper.find_element_by_xpath('//*[@id="pre-orderfeatures"]/div/div/div[9]/div[2]/div/span/span[1]')

        if element.text == 'Not Available':
            return 0
        else:
            return 1
