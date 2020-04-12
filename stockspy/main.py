#!/usr/bin/env python3

import logging
import sys
import threading
import time
import datetime
import argparse
import subprocess
import pprint
import random
import smtplib
from email.message import EmailMessage
from urllib.parse import urlparse

from flask import Flask

from vendors.vendors import Vendors
from products.products import Products

# global as the StockSpy() class and the outer Flask server need access.
results = {
    'products': [],
    'nextCheckMins': None,
    'nextCheckUTC': None
}


class StockSpy():
    global results

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

    def run(self, debug, alerts, interval_max, smtp_username, smtp_password, smtp_server):
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

                # Prevent returning empty results during checks by overwriting
                # the results global with this once we've finished.
                new_results = {
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

                    new_results['products'].append(
                        {
                            'timestamp': datetime.datetime.utcnow().isoformat(),
                            'url': url,
                            'vendor': vendor.hostname,
                            'stock': stock
                        }
                    )

                new_results['nextCheckMins'] = interval

                next_check_utc = datetime.datetime.utcnow() + datetime.timedelta(minutes=interval)
                new_results['nextCheckUTC'] = next_check_utc.isoformat()

                # Replace the results global now we've got all the data.
                results.clear()
                results.update(new_results)

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
        email = EmailMessage()
        email.set_content(content)

        email['Subject'] = f'StockSpy - STOCK AVAILABLE'
        email['From'] = smtp_username
        email['To'] = smtp_username  # TODO: Accept a list of recipients.

        smtp_client = smtplib.SMTP(smtp_server)

        smtp_client.ehlo()
        smtp_client.starttls()
        smtp_client.login(smtp_username, smtp_password)
        smtp_client.send_message(email)
        smtp_client.quit()

    def ui(self, debug):
        cmd = ''
        server = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

        while True:
            out = server.stderr.read(1)

            if out == '' and server.poll() is not None:
                break

            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()


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
    stockspy = StockSpy()

    # Start the stock checker thread.
    scrapers = threading.Thread(
        name='scrapers',
        target=stockspy.run,
        kwargs={
            'debug': args.debug,
            'alerts': args.alerts,
            'interval_max': args.interval_max,
            'smtp_username': args.smtp_username,
            'smtp_password': args.smtp_password,
            'smtp_server': args.smtp_server
        }
    )
    scrapers.start()

    # Start the Nuxt Web UI server thread.
    ui = threading.Thread(
        name='stockspyui',
        target=stockspy.ui,
        kwargs={
            'debug': args.debug
        }
    )
    ui.start()

    # Start the Flask API server.
    server = Flask(__name__)

    @server.route('/')
    def index():
        return results

    server.run(host='0.0.0.0')
