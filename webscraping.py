from math import prod
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlalchemy


searchterm = 'HP+Elitebook+840+G2'

def get_data(searchterm):
    url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_TitleDesc=0&LH_BIN=1&LH_ItemCondition=3000&rt=nc&LH_Sold=1&LH_Complete=1'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'Title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}),
            'SoldPrice': item.find('span', {'class': 's-item__price'}),
            'SoldDate': item.find('div', {'class': 's-item__title--tagblock'}),
            'ListingLink': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist):
    
    engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')

    productsdf = pd.DataFrame(productslist)
    productsdf['Title'] = productsdf['Title'].astype(str)
    productsdf['Title'] = productsdf['Title'].str.replace('<h3 class="s-item__title s-item__title--has-tags">', '', regex=False).str.replace('</h3>', '', regex=False).str.replace('<span class="LIGHT_HIGHLIGHT">New listing</span>', '', regex=False)
    productsdf.drop(productsdf.index[productsdf['Title']== 'None'], inplace=True)


    productsdf['SoldPrice'] = productsdf['SoldPrice'].astype(str)
    productsdf['SoldPrice'] = productsdf['SoldPrice'].str.replace('<span class="s-item__price">', '', regex=False).str.replace('</span>', '', regex=False).str.replace('<span class="POSITIVE">', '', regex=False).str.replace('<span class="DEFAULT POSITIVE">', '', regex=False).str.replace('£', '', regex=False).str.replace('$', '', regex=False).str.replace('<span class="POSITIVE ITALIC">', '', regex=False).str.replace('<span', '', regex=False).str.replace(',', '', regex=False)
    productsdf['SoldPrice'] = productsdf['SoldPrice'].str.split(' ').str[0]
    productsdf['SoldPrice'] = productsdf['SoldPrice'].astype(float)

    productsdf['SoldDate'] = productsdf['SoldDate'].astype(str)
    productsdf['SoldDate'] = productsdf['SoldDate'].str.replace('<div class="s-item__title--tagblock"><span class="POSITIVE">Sold  ', '', regex=False).str.replace('</span><span class="clipped">Sold item</span></div>', '', regex=False)

    productsdf['ConnectedAsset_id'] = '180'
    
    productsdf = productsdf[
        ['ConnectedAsset_id', 'Title', 'SoldPrice', 'SoldDate', 'ListingLink']
        ]
    #productsdf.to_csv('output.csv')    
    productsdf.to_sql('SWIPapp_ebaylookup',engine, if_exists='append', index=False)

    return

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist)