import os

from .common import Vendor


class Tesco(Vendor):
    """
    ENV vars:
        - SS_WWW_TESCO_COM_USER
        - SS_WWW_TESCO_COM_PASS
    """
    @Vendor.scraper
    def get_stock(self, url):
        try:
            username = os.environ['SS_WWW_TESCO_COM_USER']
            password = os.environ['SS_WWW_TESCO_COM_PASS']

        except KeyError:
            raise EnvironmentError

        # Login form: Email address.
        self.scraper.find_element_by_xpath(
            '//*[@id="username"]').send_keys(username)

        # Login form: Password.
        self.scraper.find_element_by_xpath(
            '//*[@id="password"]').send_keys(password)

        # Login form: Submit.
        self.scraper.find_element_by_xpath(
            '//*[@id="sign-in-form"]/button').click()

        # Delivery slots table.
        element = self.scraper.find_element_by_xpath(
            '//*[@id="slot-matrix"]'
        )

        if 'No slots available!' in element.text:
            return 0
        else:
            return 1
