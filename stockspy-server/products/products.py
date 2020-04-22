import json
import os


class Products():
    def __init__(self):
        pass

    def load(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', 'products.json'), 'r') as products_file:

            products_raw = products_file.read()

        return json.loads(products_raw)
