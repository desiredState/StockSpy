#!/usr/bin/env python

import argparse
import shutil
import sys
import subprocess

PROJECT_DOCKER_NAMESPACE = 'desiredstate'
PROJECT_DOCKER_TAG = 'latest'
PROJECT_DOCKER_IMAGE_SERVER = 'stockspy-server'
PROJECT_DOCKER_IMAGE_CLIENT = 'stockspy-client'


class Wrapper:
    def __init__(self):
        if not shutil.which('docker'):
            print(f'Docker is required. Please install it then try again.')
            sys.exit(1)

    def start(self):
        pass

   def stop(self):
        pass

    def logs(self):
        pass


if __name__ == '__main__':
    wrapper = Wrapper()

    parser = argparse.ArgumentParser()

    root_parser = parser.add_subparsers()
    start_parser = root_parser.add_parser('start', help='start the container')
    stop_parser = root_parser.add_parser('stop', help='stop the container')
    logs_parser = root_parser.add_parser('logs', help='tail container logs')

    parser.parse_args()
