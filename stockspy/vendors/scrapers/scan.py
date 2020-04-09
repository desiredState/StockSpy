from .common import Vendor


class Scan(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        element = self.scraper.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div[3]/div/span/a')

        if element.text == 'Pre Order':
            print('found')
            return 0
        else:
            return 1
