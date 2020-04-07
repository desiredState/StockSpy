#!/usr/bin/env python3

import logging
import sys
import time
import argparse
import os
import smtplib

from vendors.vendors import Vendors
from products.products import Products


class StockSpy():
    def __init__(self):
        try:
            logging.basicConfig(
                format='[%(asctime)s] StockSpy (%(levelname)s) > %(message)s',
                datefmt='%H:%M:%S',
                level=logging.INFO
            )

            self.logger = logging.getLogger('stockspy')

        except Exception as e:
            print(f'Failed to initialise logging with exception:\n{e}')
            sys.exit(1)

    def run(self, debug, interval, silent):
        log = self.logger

        if debug:
            log.setLevel(logging.DEBUG)
            log.debug('Debug on.')

        if not silent:
            # Audio support (for alarms). pygame must be imported after setting the
            # environment variable to prevent it spamming STDOUT.
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
            import pygame

            pygame.init()
            self.alarm = pygame.mixer.Sound('assets/alarm.wav')

        vendors = Vendors()
        products = Products()

        # Main loop.
        while True:
            try:
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
                        self.alert(product, silent)

                log.info(f'Checking again in {interval} minute(s)...')
                time.sleep(interval * 60)

            except KeyboardInterrupt:
                log.info('Exiting...')
                sys.exit(0)

            except Exception as e:
                log.error(f'An error occured:\n{e}')
                continue

    def alert(self, product, silent):
        log = self.logger
        log.info(f'STOCK AVAILABLE: {list(product.keys())[0]}')

        self.send_email(f'STOCK AVAILABLE: {list(product.keys())[0]}')

        if not silent:
            self.alarm.play()

    def send_email(self, content):
        from email.message import EmailMessage

        msg = EmailMessage()
        msg.set_content(content)

        msg['Subject'] = f'StockSpy - STOCK AVAILABLE'
        msg['From'] = 'me'
        msg['To'] = 'you'

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()


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

    parser.add_argument(
        '-s',
        '--silent',
        required=False,
        action='store_true',
        help='don\'t play an alarm sound (default: False)',
        default=False
    )

    args = parser.parse_args()

    spy = StockSpy()
    spy.run(
        debug=args.debug,
        interval=args.interval,
        silent=args.silent
    )
