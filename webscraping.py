from math import prod
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlalchemy


searchterm = input("Type what you searching for: ")
searchterm.replace(" ", "+")

def get_data(searchterm):
    url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_TitleDesc=0&LH_BIN=1&LH_ItemCondition=3000&rt=nc&LH_Sold=1&LH_Complete=1&LH_ItemCondition=3000'
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
    for item in results:
        product = {
            'Title': item.find('div', {'class': 's-item__title'}).text,
            'SoldPrice': item.find('span', {'class': 's-item__price'}),
            'SoldDate': item.find('div', {'class': 's-item__title--tagblock'}),
            'ListingLink': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist):
    
    #engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')

    productsdf = pd.DataFrame(productslist)
    productsdf['Title'] = productsdf['Title'].astype(str)
    productsdf['Title'] = productsdf['Title'].str.replace('<div class="s-item__title s-item__title--has-tags"><span aria-level="3" role="heading">', '', regex=False).str.replace('</span></div>', '', regex=False)
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
    
    rowcount = productsdf.shape[0]
    print("Found items: " + str(rowcount))
    todelete = round(0.05*rowcount)
    print("Deleting top and bottom: " + str(todelete))

    productsdf = productsdf.drop(productsdf.head(todelete).index)
    productsdf = productsdf.drop(productsdf.tail(todelete).index)

    median = productsdf['SoldPrice'].median()
    print("Price median: £" + str(median))

    Neat = round(0.3* median)
    Good = round(0.15* median)
    Faulty = round(0.05* median)

    print("Neat offer: £" + str(Neat))
    print("Good offer: £" + str(Good))
    print("Faulty or locked offer: £" + str(Faulty))

    productsdf.to_csv('output2.csv')   
    #productsdf.to_sql('SWIPapp_ebaylookup',engine, if_exists='append', index=False)

    return

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist)