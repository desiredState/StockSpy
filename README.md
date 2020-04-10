# StockSpy

## Installation (Linux)

```sh
sudo curl -fsSL https://raw.githubusercontent.com/desiredState/StockSpy/master/wrapper.sh -o /usr/local/bin/stockspy && sudo chmod 755 /usr/local/bin/stockspy
```

```sh
stockspy --help
```

## Adding a new Product/Vendor

1. If you have any, add the new product(s) to the `products.json` file.
2. Add a new `<vendor>.py` file in `vendors/scrapers/` containing something like:

```python
from .common import Vendor


class SomeVendor(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        """ Return more than 0 if the product is available. """
        if 'Out of stock' not in self.scraper.page_source:
            return 1
        else:
            return 0

```

3. At the relevant parts of the `vendors/vendors.py` file import the above new module, instantiate an object and drop in an `elif` like:

```python
from .scrapers.somevendor import SomeVendor
```

```python
self.somevendor = SomeVendor()
```

```python
elif vendor == 'www.somevendor.com':
    stock = self.somevendor.get_stock(url)
```
