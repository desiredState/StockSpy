from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException


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

            # Request page content.
            self.scraper.get(url)

            # Prevent some scraper identification techniques.
            # https://intoli.com/blog/making-chrome-headless-undetectable/
            self.scraper.execute_script("""
Object.defineProperty(navigator, 'languages', {
  get: function() {
    return ['en-US', 'en'];
  },
});

Object.defineProperty(navigator, 'plugins', {
  get: function() {
    return [1, 2, 3, 4];
  },
});

const getParameter = WebGLRenderingContext.getParameter;

WebGLRenderingContext.prototype.getParameter = function(parameter) {
  if (parameter === 37445) {
    return 'Intel Open Source Technology Center';
  }

  if (parameter === 37446) {
    return 'Mesa DRI Intel(R) Ivybridge Mobile ';
  }

  return getParameter(parameter);
};
""")

            # Run the vendor-specific scraping function which is wrapped by
            # this decorator.
            try:
                stock = func(self, url)

            except NoSuchElementException:
                stock = 'error'

            self.scraper.close()
            self.scraper.quit()

            return stock

        return wrapper
