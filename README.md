# StockSpy

StockSpy is a modular stock monitoring and alerting platform.

## Installation

StockSpy is distributed via Docker, so ensure you have that installed before continuing.

```bash
$ sudo curl -fsSL https://raw.githubusercontent.com/desiredState/StockSpy/master/wrapper.sh -o /usr/local/bin/stockspy && sudo chmod 755 /usr/local/bin/stockspy
```

```bash
$ stockspy start server
$ stockspy start client
```

Once started, StockSpy logs can be observed like so:

```bash
$ stockspy logs server
$ stockspy logs client
```

To stop and remove StockSpy, again, just use Docker commands:

```bash
$ stockspy stop server
$ stockspy stop client
```

## Adding a new Product/Vendor

1. Add the new product URL(s) to the `stockspy-server/products.json` file.
2. Add a new `<vendor>.py` file in the `stockspy-server/vendors/scrapers/` directory, containing something like:

```python
from .common import Vendor


class SomeVendor(Vendor):
    @Vendor.scraper
    def get_stock(self, url):
        # Find the element which hints at a "no stock" condition.
        element = self.scraper.find_element_by_xpath('//*[some_element]')

        # Return 0 (stock) if we find an "out of stock" message of some kind.
        if 'out of stock' in element.text:  # Change to match the site's text.
            return 0
        else:
            # Otherwise, returning anything >0 will trigger a stock alert.
            # You could find and return the actual stock level here but if
            # all you care about is getting an alert it's unnecessary.
            return 1

```

3. At the relevant parts of the `stockspy-server/vendors/vendors.py` file import the above new module, instantiate an object and drop in an `elif` like so:

```python
from .scrapers.somevendor import SomeVendor
```

```python
self.somevendor = SomeVendor()
```

```python
elif vendor.hostname == 'www.somevendor.com':
    stock = self.somevendor.get_stock(url)
```

4. To build and test a new Docker Image use the `factory.sh` script:

```bash
$ ./factory.sh --help
```
