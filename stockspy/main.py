#!/usr/bin/env python3

import logging
import sys
import time
import argparse
import os
import random
import smtplib
from email.message import EmailMessage
from urllib.parse import urlparse

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

    def run(self, debug, interval_max, silent, smtp_username, smtp_password, smtp_server):
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
                    vendor = urlparse(url)
                    log.info('Checking: {}'.format(vendor.hostname))

                    stock = vendors.get_stock(url)

                    if stock > 0:
                        self.alert(url, silent, smtp_username, smtp_password, smtp_server)

                    stock_dict['stock'].append({url: stock})

                log.debug(stock_dict)

                interval = random.randint(1, interval_max)

                log.info(f'Checking again in {interval} minute(s)...')
                time.sleep(interval * 60)

            except KeyboardInterrupt:
                log.info('Exiting...')
                sys.exit(0)

            except Exception as e:
                log.error(f'An error occured:\n{e}')
                log.info(f'Trying again in 5 minutes...')
                time.sleep(5 * 60)
                continue

    def alert(self, url, silent, smtp_username, smtp_password, smtp_server):
        log = self.logger
        log.info(f'STOCK AVAILABLE: {url}')

        log.info('Sending email alert...')
        self.send_email(
            f'STOCK AVAILABLE: {url}',
            smtp_username,
            smtp_password,
            smtp_server
        )

        if not silent:
            self.alarm.play()

    def send_email(self, content, smtp_username, smtp_password, smtp_server):
        msg = EmailMessage()
        msg.set_content(content)

        msg['Subject'] = f'StockSpy - STOCK AVAILABLE'
        msg['From'] = smtp_username
        msg['To'] = smtp_username

        s = smtplib.SMTP(smtp_server)
        s.ehlo()
        s.starttls()
        s.login(smtp_username, smtp_password)
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
        "--interval-max",
        required=False,
        type=int,
        metavar='MINUTES',
        help="the maximum time to wait between runs in minutes (default: 30)",
        default=30
    )

    parser.add_argument(
        '-x',
        '--silent',
        required=False,
        action='store_true',
        help='don\'t play an alarm sound (default: False)',
        default=False
    )

    parser.add_argument(
        "-u",
        "--smtp-username",
        required=True,
        type=str,
        metavar='USERNAME',
        help="SMTP username"
    )

    parser.add_argument(
        "-p",
        "--smtp-password",
        required=True,
        type=str,
        metavar='PASSWORD',
        help="SMTP password"
    )

    parser.add_argument(
        "-s",
        "--smtp-server",
        required=False,
        type=str,
        metavar='URL',
        help="SMTP server (default: smtp.gmail.com:587)",
        default='smtp.gmail.com:587'
    )

    args = parser.parse_args()

    spy = StockSpy()
    spy.run(
        debug=args.debug,
        interval_max=args.interval_max,
        silent=args.silent,
        smtp_username=args.smtp_username,
        smtp_password=args.smtp_password,
        smtp_server=args.smtp_server
    )
