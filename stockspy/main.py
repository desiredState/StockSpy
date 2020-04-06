#!/usr/bin/env python3

import logging
import sys
import time
import argparse
import os

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

        # Audio support (for alarms). pygame must be imported after setting the
        # environment variable to prevent it spamming STDOUT.
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        import pygame
        pygame.init()
        self.alarm = pygame.mixer.Sound('assets/alarm.wav')

    def run(self, debug, interval):
        log = self.logger

        if debug:
            log.setLevel(logging.DEBUG)
            log.debug('Debug on.')

        vendors = Vendors()
        products = Products()

        # Main loop.
        try:
            while True:
                products_dict = products.load()
                stock_dict = {'stock': []}

                # For each product, scrape current stock and add to stock_dict.
                for url in products_dict['products']:
                    log.info('Checking: {}'.format(vendors.get_vendor(url)))

                    stock = vendors.get_stock(url)
                    stock_dict['stock'].append({url: stock})

                log.debug(stock_dict)

                # Alert if any product in stock_dict is >0
                for product in stock_dict['stock']:
                    if list(product.values())[0] > 0:
                        log.info(f'STOCK AVAILABLE: {list(product.keys())[0]}')
                        self.alarm.play()

                log.info(f'Checking again in {interval} minute(s)...')
                time.sleep(interval * 60)

        except KeyboardInterrupt:
            log.info('Exiting...')
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
