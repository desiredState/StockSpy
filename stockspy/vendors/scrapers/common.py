from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Vendor():
    def __init__(self):
        pass

    def __call__(self):
        pass

    #
    # Decorators
    #

    def scraper(func):
        def wrapper(self, url):
            headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                       '10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                       '/77.0.3865.90 Safari/537.36'}

            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument(f'user-agent={headers}')

            self.scraper = webdriver.Chrome(options=options)

            # Retrieve page content.
            self.scraper.get(url)

            # Run vendor-specific scraping function.
            stock = func(self, url)

            self.scraper.close()

            return stock

        return wrapper