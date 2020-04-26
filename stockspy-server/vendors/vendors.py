from urllib.parse import urlparse

from .scrapers.oculus import Oculus
from .scrapers.amazonuk import AmazonUK
from .scrapers.argos import Argos
from .scrapers.currys import Currys
from .scrapers.overclockersuk import OverclockersUK
from .scrapers.scan import Scan
from .scrapers.very import Very
from .scrapers.johnlewis import JohnLewis
from .scrapers.game import Game
from .scrapers.tesco import Tesco

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
        self.game = Game()
        self.tesco = Tesco()

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

        elif vendor.hostname == 'www.game.co.uk':
            stock = self.game.get_stock(url)

        elif vendor.hostname == 'www.tesco.com':
            stock = self.tesco.get_stock(url)

        else:
            raise ValueError

        return stock
