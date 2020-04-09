from urllib.parse import urlparse

from .scrapers.oculus import Oculus
from .scrapers.amazonuk import AmazonUK
from .scrapers.argos import Argos
from .scrapers.currys import Currys
from .scrapers.overclockersuk import OverclockersUK
from .scrapers.scan import Scan
from .scrapers.very import Very
from .scrapers.johnlewis import JohnLewis

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
        self.johnlewis = JohnLewis()

    def get_stock(self, url):
        vendor = urlparse(url)

        if vendor.hostname == 'www.amazon.co.uk':
            stock = self.amazonuk.get_stock(url)

        elif vendor.hostname == 'www.argos.co.uk':
            stock = self.argos.get_stock(url)

        elif vendor.hostname == 'www.currys.co.uk':
            stock = self.currys.get_stock(url)

        elif vendor.hostname == 'www.oculus.com':
            stock = self.oculus.get_stock(url)

        elif vendor.hostname == 'www.overclockers.co.uk':
            stock = self.overclockersuk.get_stock(url)

        elif vendor.hostname == 'www.scan.co.uk':
            stock = self.scan.get_stock(url)

        elif vendor.hostname == 'www.very.co.uk':
            stock = self.very.get_stock(url)

        elif vendor.hostname == 'www.johnlewis.com':
            stock = self.johnlewis.get_stock(url)

        return stock
