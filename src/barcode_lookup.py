from googlesearch import search
from urllib.request import Request, urlopen
import logging
import json
import bs4


def find_product(barcode):
    barcode = str(barcode).replace('b\'', '').replace('\'', '')
    print('Searching for {}'.format(barcode))
    for url in search(barcode, tld="co.in", num=10, stop=10, pause=2):
        if 'meny.no' in url:
            print('Gathering data from meny.no: {}'.format(url))
            try:
                return find_productinfo_meny(url)
            except:
                logging.info('Failed in finding product data from EA: {} from meny'.format(barcode))
                continue
        if 'spar.no' in url:
            print('Gathering data from spar.no')
            try:
                return find_productinfo_spar(url)
            except:
                logging.info('Failed in finding product data from EA: {} from spar'.format(barcode))
                continue


def find_productinfo_meny(url):
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(request_site)
    soup = bs4.BeautifulSoup(html, features='html.parser')
    maincontent = soup.find('main', {'id': 'maincontent'}).div

    return build_product_info(maincontent, 'meny')


def find_productinfo_spar(url):
    print(url)
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(request_site)
    soup = bs4.BeautifulSoup(html, features='html.parser')
    product_article = soup.find_all('article', class_='cw-product-detail-wrapper')[0].div
    return build_product_info(product_article, 'spar')


def build_product_info(productinfo_element, datasource):
    product_info_json = json.loads(productinfo_element['data-prop-product'])

    return {
        'title': product_info_json['title'],
        'price': product_info_json['pricePerUnit'],
        'barcode_id': product_info_json['id'],
        'data_source': datasource
    }
