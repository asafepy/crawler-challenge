import csv

from config.config_file import appconfig
from core.db.database import get_engine_db
from core.utils.file_util import create_file
from core.db.products import Product_db


__author__ = 'asafe'


class Indexer(object):
    _test = False

    @classmethod
    def export_data_to_csv(cls, file_name, products):

        header = ['nome_do_produto', 'título', 'url']
        create_file(file_name, header)
        keys = []
        with open(file_name, 'a') as csvfile:
            for product in products:
                spam = csv.writer(csvfile, delimiter=',')
                spam.writerow([product.name, product.title, product.url])
                keys.append(product.id)

        Product_db(get_engine_db(cls._test)).update_status_products(keys, 'INDEXED')

if __name__ == '__main__':
    
    product_db = Product_db(get_engine_db())
    products = product_db.get_products_for_status('PROCESSED')
    Indexer.export_data_to_csv(appconfig['local_file_name'], products)