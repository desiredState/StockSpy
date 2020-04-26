import os

from .common import Vendor


class Tesco(Vendor):
    """
    ENV variables:
        - SS_WWW_TESCO_COM_USER (str)
        - SS_WWW_TESCO_COM_PASS (str)
    """
    @Vendor.scraper
    def get_stock(self, url):
        username = os.getenv('SS_WWW_TESCO_COM_USER')
        password = os.getenv('SS_WWW_TESCO_COM_PASS')

        element = self.scraper.find_element_by_xpath(
            '//*[@id="slot-matrix"]/div[3]/div[2]/div/div/div[2]/div'
        )

        if 'No slots available!' in element.text:
            return 0
        else:
            return 1
