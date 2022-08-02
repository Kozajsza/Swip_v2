from multiprocessing import Value
from ntpath import join
from django.shortcuts import render, redirect
from .models import Order, Asset, AssetLog, ebayLookup, Lists
from django.db.models import Avg, Max, Min
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateNewAsset, CreateNewOrder, CreateNewLog, CreateNewList
import sqlalchemy
import pandas as pd
import glob
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Create your views here.

# THIS IS THE HOME PAGE - DISPLAYS SEARCH + LIST OF RECENTLY CREATED AND EDITED ASSETS:


def navbar(request):
    return render (request, 'SWIPsite/navbar.html')

def home(request):
    return render (request, 'SWIPapp/home.html')

def login(request):
    return render (request, 'SWIPapp/login.html')

def assetlabel(request,id):
    asset = Asset.objects.get(id=id)
    context = {
        'asset':asset,
    }

    return render(request, 'SWIPapp/assetlabel.html', context)

def assets(request):
    asset = Asset.objects.order_by('-Created')
    if request.method == 'POST':
        files=request.FILES.getlist("myfile")
        date = datetime.now()
        df = pd.concat(
            map(pd.read_csv, files), ignore_index=True) #this concats selected files into one dataframe and ignores the 1st row

        engine = sqlalchemy.create_engine('sqlite:///db.sqlite3') #this loads up the engine for sqlalchemy
        
         # RULES TO CLEAN UP THE BASIC INFO
        df['Order_Number_id'] = df['user4']
        df['Asset_QR'] = df['user3']
        df['Type'] = ''
        df['Make'] = df['Computer Vendor']
        df['Make'] = df['Make'].str.replace('Inc.', '', regex=False)
        df['Make'] = df['Make'].str.replace('Hewlett-Packard', 'HP', regex=False) 
        df['Model'] = df['Computer Model']
        df['Model'] = df['Model'].str.replace('HP', '', regex=False)
        df['Serial_Number'] = df['Computer Serial']

            # RULES TO CLEAN UP CPU SYNTAX
        df[['CPU', 'CPUx']] = df['CPU 1'].str.split(',', n=1, expand=True)
        df['CPU'] = df['CPU'].str.replace('(R)', '', regex=False)
        df['CPU'] = df['CPU'].str.replace('(TM)', '', regex=False)
        df[['RAM', 'RAMx']] = df['RAM'].str.split(' ', n=1, expand=True)

            # RULES TO CLEAN UP RAM SYNTAX AND TURN INTO INTEGER
        df['RAM'] = df['RAM'].astype(int)
        df['RAM'] = df['RAM'].div(1024)

            # RULES TO CLEAN UP STORAGE INFO
        df['Storage'] = df['Vendor'] + ' ' + df['Drive Model']
        df['Storage_Serial_Number'] = df['Drive Serial']

            # RULES TO CLEAN UP THE STORAGE CAPACITY SYNTAX, TURN IT INTO INTEGER AND ROUND UP TO FULL NUMBER
        df[['Storage_Capacity', 'STRx']] = df['Drive Size'].str.split('.', n=1, expand=True)
        df['Storage_Capacity'] = df['Storage_Capacity'].astype(int)
        df['Storage_Capacity'] = df['Storage_Capacity'].div(1024)
        df['Storage_Capacity'] = df['Storage_Capacity'].round(decimals=0)

            # RULES FOR CLEANING UP THE GPU SYNTAX
        df['GPU'] = df['Video Card 1'].str.replace('Vendor:', '')
        df['GPU'] = df['GPU'].str.replace(', Product:', '', regex=False)
        df['GPU'] = df['GPU'].str.replace('Advanced Micro Devices, Inc. ', '', regex=False)
        df['GPU'] = df['GPU'].str.replace('[', '', regex=False)
        df['GPU'] = df['GPU'].str.replace(']', '', regex=False)

        df['Motherboard_Test'] = df['Motherboard Test']
        df['CPU_Test'] = df['Processor Test']
        df['RAM_Test'] = df['Memory Test']

        df['Wipe_Method'] = df['Wipe Pattern']
        df['Wipe_Start_Time'] = df['Action Start Time']
        df['Wipe_End_Time'] = df['Action End Time']
        df['Wipe_Result'] = df['Action Result']
        df['Weight'] = ''
        df['Ecommerce_Title']= df['Make'] + ' ' + df['Model'] + ' ' + df['CPU'] + ' ' + df['RAM'].astype(str) + 'GB RAM' + df['Storage_Capacity'].astype(str)
        df['Ecommerce_Category']=''
        df['Ecommerce_Condition']=''
        df['Ecommerce_Condition_Description']=''
        df['Ecommerce_Item_Description']=''
        df['Ecommerce_Price']='0'
        df['Created'] = date
        df['Updated'] = date

        # CREATING NEW CLEANED UP DATA TABLE
        df = df[
            [
                'Order_Number_id', 'Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                'GPU', 'Motherboard_Test', 'CPU_Test', 'RAM_Test', 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result',
                'Weight', 'Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Condition_Description', 'Ecommerce_Item_Description', 'Ecommerce_Price',
                'Created', 'Updated'
            ]
        ]
        df = df.drop_duplicates(subset='Serial_Number', keep="first") #for some reason pandas sometimes duplicates some of the files, this drops duplicate records
        df.to_sql('SWIPapp_asset',engine, if_exists='append', index=False)



    context={
        'asset':asset,
    }

    return render (request, 'SWIPapp/assets.html', context)


def orders(request):
    order = Order.objects.filter()[:20]
    form = CreateNewOrder()
    context = {'order':order,
                'form':form,
                }

    if request.method == 'POST':
        form = CreateNewOrder(request.POST)
        if form.is_valid():
            form.save()


    return render(request, 'SWIPapp/orders.html', context)
    

# THIS IS WHAT IS GOING TO BE DISPLAYED ON ORDER PAGE:
def orderindex(request, id):
    order = Order.objects.get(id=id)
    asset = Asset.objects.filter(Order_Number_id=order)
    OrderID = Order.objects.filter(id=id).values('id')[0]['id']
    date = datetime.now()
    #hdds = HDD.objects.filter(Order_Number_id=order)
    if request.method == 'POST':
        files=request.FILES.getlist("myfile")
        df = pd.concat(
            map(pd.read_csv, files), ignore_index=True) #this concats selected files into one dataframe and ignores the 1st row

        engine = sqlalchemy.create_engine('sqlite:///db.sqlite3') #this loads up the engine for sqlalchemy
        
         # RULES TO CLEAN UP THE BASIC INFO
        df['Order_Number_id'] = df['user4']
        df['Order_Number_id'] = OrderID
        df['Asset_QR'] = df['user3']
        df['Type'] = ''
        df['Make'] = df['Computer Vendor']
        df['Make'] = df['Make'].str.replace('Inc.', '', regex=False)
        df['Make'] = df['Make'].str.replace('Hewlett-Packard', 'HP', regex=False) 
        df['Model'] = df['Computer Model']
        df['Model'] = df['Model'].str.replace('HP', '', regex=False)
        df['Serial_Number'] = df['Computer Serial']

            # RULES TO CLEAN UP CPU SYNTAX
        df[['CPU', 'CPUx']] = df['CPU 1'].str.split(',', n=1, expand=True)
        df['CPU'] = df['CPU'].str.replace('(R)', '', regex=False)
        df['CPU'] = df['CPU'].str.replace('(TM)', '', regex=False)
        df[['RAM', 'RAMx']] = df['RAM'].str.split(' ', n=1, expand=True)

            # RULES TO CLEAN UP RAM SYNTAX AND TURN INTO INTEGER
        df['RAM'] = df['RAM'].astype(int)
        df['RAM'] = df['RAM'].div(1024)

            # RULES TO CLEAN UP STORAGE INFO
        df['Storage'] = df['Vendor'] + ' ' + df['Drive Model']
        df['Storage_Serial_Number'] = df['Drive Serial']

            # RULES TO CLEAN UP THE STORAGE CAPACITY SYNTAX, TURN IT INTO INTEGER AND ROUND UP TO FULL NUMBER
        df[['Storage_Capacity', 'STRx']] = df['Drive Size'].str.split('.', n=1, expand=True)
        df['Storage_Capacity'] = df['Storage_Capacity'].astype(int)
        df['Storage_Capacity'] = df['Storage_Capacity'].div(1024)
        df['Storage_Capacity'] = df['Storage_Capacity'].round(decimals=0)

            # RULES FOR CLEANING UP THE GPU SYNTAX
        df['GPU'] = df['Video Card 1'].str.replace('Vendor:', '')
        df['GPU'] = df['GPU'].str.replace(', Product:', '', regex=False)
        df['GPU'] = df['GPU'].str.replace('Advanced Micro Devices, Inc. ', '', regex=False)
        df['GPU'] = df['GPU'].str.replace('[', '', regex=False)
        df['GPU'] = df['GPU'].str.replace(']', '', regex=False)

        df['Motherboard_Test'] = df['Motherboard Test']
        df['CPU_Test'] = df['Processor Test']
        df['RAM_Test'] = df['Memory Test']

        df['Wipe_Method'] = df['Wipe Pattern']
        df['Wipe_Start_Time'] = df['Action Start Time']
        df['Wipe_End_Time'] = df['Action End Time']
        df['Wipe_Result'] = df['Action Result']
        df['Weight'] = ''
        df['Ecommerce_Title']= df['Make'] + ' ' + df['Model'] + ' ' + df['CPU']  + ' ' + df['RAM'].astype(str) + 'GB RAM'
        df['Ecommerce_Title'] = df['Ecommerce_Title'].str.replace('.0', '', regex=False)
        df['Ecommerce_Category']=''
        df['Ecommerce_Condition']=''
        df['Ecommerce_Condition_Description']=''
        df['Ecommerce_Item_Description']=''
        df['Ecommerce_Price']='0'
        df['Created'] = date
        df['Updated'] = date

        # CREATING NEW CLEANED UP DATA TABLE
        df = df[
            [
                'Order_Number_id', 'Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                'GPU', 'Motherboard_Test', 'CPU_Test', 'RAM_Test', 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result',
                'Weight', 'Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Condition_Description', 'Ecommerce_Item_Description', 'Ecommerce_Price',
                'Created', 'Updated'
            ]
        ]
        df = df.drop_duplicates(subset='Serial_Number', keep="first") #for some reason pandas sometimes duplicates some of the files, this drops duplicate records
        df.to_sql('SWIPapp_asset',engine, if_exists='append', index=False)

    context = {'order':order,
                'asset':asset,
                #'hdds':hdds,
                }

    return render(request, 'SWIPapp/orderindex.html', context)

def orderreport(request, id):
    order = Order.objects.get(id=id)
    asset = Asset.objects.filter(Order_Number_id=order)

    context = {'order':order,
                'asset':asset,
                #'hdds':hdds,
                }

    return render(request, 'SWIPapp/orderreport.html', context)


def updateorder(request, id):
    order = Order.objects.get(id=id)
    form = CreateNewOrder(instance=order)

    if request.method == 'POST':
        form = CreateNewOrder(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect("/order/{id}/".format(id=id))

    context = {'form':form}
    return render(request, 'SWIPapp/updateorder.html', context)

def deleteorder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect ('orders')
    
    context = {'order':order}

    return render (request, 'SWIPapp/deleteorder.html', context)


def assetindex(request, id):
    asset = Asset.objects.get(id=id)
    
    
    context = {
        'asset':asset,
            }


    return render(request, 'SWIPapp/assetindex.html', context)

def assetindexecommerce (request, id):
    asset = Asset.objects.get(id=id)
    ebayitem = ebayLookup.objects.filter(ConnectedAsset_id=asset)
    AssetMake = Asset.objects.filter(id=id).values('Make')[0]['Make']
    AssetModel = Asset.objects.filter(id=id).values('Model')[0]['Model']
    AssetID = Asset.objects.filter(id=id).values('id')[0]['id']

    #Grabbing the average price, transforming it into a list and then into float and rounding it up to 2 decimal places:
    ebayitemavg = ebayLookup.objects.filter(ConnectedAsset_id=asset).aggregate(Avg('SoldPrice')).values()
    ebayitemmax = ebayLookup.objects.filter(ConnectedAsset_id=asset).aggregate(Max('SoldPrice')).values()
    ebayitemmin = ebayLookup.objects.filter(ConnectedAsset_id=asset).aggregate(Min('SoldPrice')).values()

    averageprice = list(ebayitemavg)
    maxprice = list(ebayitemmax)
    minprice = list(ebayitemmin)
    
    for i in averageprice:
        if i is None:
            y = 0
        else:
            x = float(i)
            y = round(x,2)

    for j in maxprice:
        if j is None:
            max = 0
        else:
            z=float(j)
            max = round(z,2)

    for k in minprice:
        if k is None:
            min = 0
        else:
            a=float(k)
            min = round(a,2)

    ebayitemcount = ebayLookup.objects.filter(ConnectedAsset_id=asset).count

    for item in ebayLookup.objects.values_list('ListingLink', flat=True).distinct():
        ebayLookup.objects.filter(pk__in=ebayLookup.objects.filter(ListingLink=item).values_list('ListingLink', flat=True)[1:]).delete() #this currently doesn't work - it should delete old records before generating new ones

    def eBay():
        if request.method == 'POST':
                df = pd.DataFrame.from_records(Asset.objects.filter(id=id).values('Make', 'Model'))
                df['Make'] = AssetMake
                df['Make'] = df['Make'].astype(str)
                df['Model'] = AssetModel
                df['Model'] = df['Model'].astype(str)
                df['Search'] = df['Make'] + df['Model']
                df['Search'] = df['Search'].str.replace(' ', '+', regex=False)
                df['Search'] = df['Search']
                df = df['Search']
                searchterm = df.to_string(index=False)
            
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

                    productsdf['ConnectedAsset_id'] = AssetID
                    
                    productsdf = productsdf[
                        ['ConnectedAsset_id', 'Title', 'SoldPrice', 'SoldDate', 'ListingLink']
                        ]

                    productsdf.to_sql('SWIPapp_ebaylookup',engine, if_exists='append', index=False)

                    

                soup = get_data(searchterm)
                productslist = parse(soup)
                output(productslist)

   

    context = {
        'asset':asset,
        'ebayitem': ebayitem,
        'ebayitemavg':y,
        'ebayitemcount':ebayitemcount,
        'ebayitemmax':max,
        'ebayitemmin':min,
        'ebaysearch':eBay,
            }

    return render(request, 'SWIPapp/assetindexecommerce.html', context)

def createasset(request):
    form = CreateNewAsset()
    context = {
        'form':form
    }

    if request.method == 'POST':
        form = CreateNewAsset()
        if form.is_valid:
            form.save()
            return('SWIPapp/assets.html')
    
    return render(request, 'SWIPapp/createasset.html', context)

# THIS IS ASSET CREATE PAGE WITH FIELDS ALREADY FILLED SO THE ASSET CAN BE UPDATED:
def updateasset(request, id):
    asset = Asset.objects.get(id=id)
    form = CreateNewAsset(instance=asset)

    if request.method == 'POST':
        form = CreateNewAsset(request.POST, instance=asset)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect("/asset/{id}/".format(id=id))

    context = {'form':form}
    return render(request, 'SWIPapp/createasset.html', context)

# THIS IS ASSET DELETE PAGE THAT ASKS FOR CONFIRMATION TO DELETE AN ASSET:
def deleteasset(request, id):
    asset = Asset.objects.get(id=id)
    if request.method == 'POST':
        asset.delete()
        return redirect ('assets')
    
    context = {'asset':asset}

    return render (request, 'SWIPapp/deleteasset.html', context)


def lists(request):

    list = Lists.objects.filter()[:20]
    form = CreateNewList()

    if request.method == 'POST':
        form = CreateNewList(request.POST)
        if form.is_valid():
            form.save()

    context = {'list':list,
                'form':form
    }

    return render (request, 'SWIPapp/lists.html', context)

def listindex(request, id):
    list = Lists.objects.get(id=id)
    asset = Lists.objects.get(id=id).AttachedAssets.filter()




    context = {
        'list':list,
        'asset':asset
    }

    return render (request, 'SWIPapp/listindex.html', context)