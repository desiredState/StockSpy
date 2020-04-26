from .common import Vendor


class Tesco(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath(
            '//*[@id="slot-matrix"]/div[3]/div[2]/div/div/div[2]/div'
        )

        if 'No slots available!' in element.text:
            return 0
        else:
            return 1
