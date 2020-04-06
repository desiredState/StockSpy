#!/usr/bin/env python3

import logging
import sys
import time
import argparse

from playsound import playsound

from vendors.vendors import Vendors
from products.products import Products


class StockSpy():
    def __init__(self):
        try:
            logging.basicConfig(
                format='StockSpy (%(levelname)s) > %(message)s',
                level=logging.INFO
            )

            self.logger = logging.getLogger('stockspy')

        except Exception as e:
            print(f'Failed to initialise logging with exception:\n{e}')
            sys.exit(1)

    def run(self, debug, interval):
        log = self.logger

        if debug:
            log.setLevel(logging.DEBUG)
            log.debug('Debug on.')

        vendors = Vendors()
        products = Products()

        # Main loop.
        try:
            log.info('Starting...')

            while True:
                products_dict = products.load()
                stock_dict = {'stock': []}

                # For each product, scrape current stock and add to stock_dict.
                for url in products_dict['products']:
                    stock = vendors.get_stock(url)
                    stock_dict['stock'].append({url: stock})

                log.debug(stock_dict)

                # Alert if any product in stock_dict is >0
                for product in stock_dict['stock']:
                    if list(product.values())[0] > 0:
                        log.info(f'STOCK AVAILABLE: {list(product.keys())[0]}')
                        playsound('static/alarm.wav', block=False)

                log.info(f'Checking again in {interval} minute(s)...')
                time.sleep(interval * 60)

        except KeyboardInterrupt:
            log.info('Stopping...')
            sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-d',
        '--debug',
        required=False,
        action='store_true',
        help='set logging level to debug (default: False)',
        default=False
    )

    parser.add_argument(
        "-i",
        "--interval",
        required=False,
        type=int,
        metavar='MINUTES',
        help="how often to run in minutes (default: 30)",
        default=30
    )

    args = parser.parse_args()

    spy = StockSpy()
    spy.run(
        debug=args.debug,
        interval=args.interval
    )
