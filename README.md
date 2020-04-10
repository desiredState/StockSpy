# StockSpy

## Installation (Linux)

StockSpy is distributed via Docker, so ensure you have that installed before continuing.

```bash
sudo curl -fsSL https://raw.githubusercontent.com/desiredState/StockSpy/master/wrapper.sh -o /usr/local/bin/stockspy && sudo chmod 755 /usr/local/bin/stockspy
```

```bash
stockspy --help
```

Once started, StockSpy logs can be observed like so:

```bash
docker logs -f stockspy
```

To stop and remove StockSpy, again, just use Docker commands:

```bash
docker rm -f stockspy
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

4. Build a new Docker Image:

```bash
./factory --help
```
