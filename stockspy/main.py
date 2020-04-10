#!/usr/bin/env python3

import logging
import sys
import time
import datetime
import argparse
import os
import pprint
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

    def run(self, debug, server, alerts, interval_max, smtp_username, smtp_password, smtp_server):
        log = self.logger

        print('\nStockSpy by desiredState.io\n')

        if debug:
            log.setLevel(logging.DEBUG)
            log.debug('Debug on.')

        if alerts:
            log.info('Alerts on.')

        log.info(f'Maximum interval (mins): {interval_max}')

        vendors = Vendors()
        products = Products()

        # Main loop.
        while True:
            try:
                interval = random.randint(1, interval_max)
                product_urls = products.load()
                results = {
                    'products': [],
                    'nextCheckMins': None,
                    'nextCheckUTC': None
                }

                # Product loop.
                for url in product_urls['products']:
                    vendor = urlparse(url)
                    log.info('Checking: {}'.format(vendor.hostname))

                    stock = vendors.get_stock(url)

                    # Alert condition.
                    if stock > 0:
                        log.info(f'STOCK AVAILABLE: {url}')

                        if alerts:
                            self.alert(url, smtp_username, smtp_password, smtp_server)

                    results['products'].append(
                        {
                            'timestamp': datetime.datetime.utcnow().isoformat(),
                            'url': url,
                            'vendor': vendor.hostname,
                            'stock': stock
                        }
                    )

                results['nextCheckMins'] = interval

                next_check_utc = datetime.datetime.utcnow() + datetime.timedelta(minutes=interval)
                results['nextCheckUTC'] = next_check_utc.isoformat()

                log.debug(pprint.pformat(results))

                log.info(f'Checking again in {interval} minutes(s)...')
                time.sleep(interval * 60)

            except KeyboardInterrupt:
                log.info('Exiting...')
                sys.exit(0)

            except Exception as e:
                log.error(f'An error occured:\n{e}')
                log.info(f'Trying again in 5 minutes...')
                time.sleep(5 * 60)
                continue

    def alert(self, url, smtp_username, smtp_password, smtp_server):
        log = self.logger

        log.info('Sending email alert...')
        self.send_email(
            f'STOCK AVAILABLE: {url}',
            smtp_username,
            smtp_password,
            smtp_server
        )

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
        '-l',
        '--server',
        required=False,
        action='store_true',
        help='run the StockSpy API server (default: False)',
        default=False
    )

    parser.add_argument(
        '-a',
        '--alerts',
        required=False,
        action='store_true',
        help='execute stock alerts, e.g, emails (default: False)',
        default=False
    )

    parser.add_argument(
        "-i",
        "--interval-max",
        required=False,
        type=int,
        metavar='MINUTES',
        help="the maximum time to wait between runs in minutes (default: 5)",
        default=5
    )

    parser.add_argument(
        "-u",
        "--smtp-username",
        required=False,
        type=str,
        metavar='USERNAME',
        help="SMTP username"
    )

    parser.add_argument(
        "-p",
        "--smtp-password",
        required=False,
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
        server=args.server,
        alerts=args.alerts,
        interval_max=args.interval_max,
        smtp_username=args.smtp_username,
        smtp_password=args.smtp_password,
        smtp_server=args.smtp_server
    )
