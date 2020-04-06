from urllib.parse import urlparse

from .scrapers.oculus import Oculus
from .scrapers.amazonuk import AmazonUK
from .scrapers.argos import Argos
from .scrapers.currys import Currys
from .scrapers.overclockersuk import OverclockersUK
from .scrapers.scan import Scan
from .scrapers.very import Very

from products.products import Products


class Vendors():
    def __init__(self):
        self.products = Products()

        self.oculus = Oculus()
        self.amazonuk = AmazonUK()
        self.argos = Argos()
        self.currys = Currys()
        self.overclockersuk = OverclockersUK()
        self.scan = Scan()
        self.very = Very()

    def get_vendor(self, url):
        vendor = urlparse(url)
        return vendor.hostname

    def get_stock(self, url):
        vendor = self.get_vendor(url)

        if vendor == 'www.amazon.co.uk':
            stock = self.amazonuk.get_stock(url)

        elif vendor == 'www.argos.co.uk':
            stock = self.argos.get_stock(url)

        elif vendor == 'www.currys.co.uk':
            stock = self.currys.get_stock(url)

        elif vendor == 'www.oculus.com':
            stock = self.oculus.get_stock(url)

        elif vendor == 'www.overclockers.co.uk':
            stock = self.overclockersuk.get_stock(url)

        elif vendor == 'www.scan.co.uk':
            stock = self.scan.get_stock(url)

        elif vendor == 'www.very.co.uk':
            stock = self.very.get_stock(url)

        return stock
