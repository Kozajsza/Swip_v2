from multiprocessing import Value
from ntpath import join
from django.shortcuts import render, redirect
from .models import Order, Asset, AssetLog, ebayLookup, Lists, HDD
from django.db.models import Avg, Max, Min
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .forms import CreateNewAsset, CreateNewOrder, CreateNewLog, CreateNewList, AssetEcommerce
import sqlalchemy
import pandas as pd
import glob
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import csv
import random
import numpy as np
import lxml

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab_qrcode import QRCodeImage

# Create your views here.

# THIS IS THE HOME PAGE - DISPLAYS SEARCH + LIST OF RECENTLY CREATED AND EDITED ASSETS:


def navbar(request):
    return render (request, 'SWIPsite/navbar.html')

def searchresults(request):
    if request.method == 'POST':
        query = request.POST['query']

        assets = Asset.objects.filter(Asset_QR__contains=query)

        context = {'query':query,
        'assets':assets,}
        return render (request, 'SWIPapp/searchresults.html', context)
    else:
        context = {}
        return render (request, 'SWIPapp/searchresults.html', context)        





def home(request):
    asset = Asset.objects.all()
    order = Order.objects.all()



    context = {
        'asset':asset,
        'order':order,
    }

    return render (request, 'SWIPapp/home.html', context)

def login(request):
    return render (request, 'SWIPapp/login.html')

def assetlabel(request,id):
    asset = Asset.objects.get(id=id)
    buf = io.BytesIO()
    pagesize = (89 * mm, 41 * mm)
    c = canvas.Canvas(buf, pagesize = pagesize, bottomup=0)
    

    textob = c.beginText()
    textob.setTextOrigin(36 * mm, 12 * mm)
    textob.setFont("Helvetica", 6)
    assetmaininfo = asset.Make + ' ' + asset.Model
    assetmeminfo = str(asset.RAM) + ' GB RAM'
    assetstoragecap = 'Storage Capacity: ' + str(asset.Storage_Capacity) + " GB"
    

    qr = QRCodeImage(asset.Asset_QR, size = 38 * mm)
    qr.drawOn(c, 0, 0)

    lines = []

    lines.append(asset.Asset_QR)
    lines.append(assetmaininfo)
    lines.append(asset.Serial_Number)
    lines.append(asset.CPU)
    lines.append(assetmeminfo)
    lines.append(asset.Storage)
    lines.append(assetstoragecap)

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    
    c.showPage()
    c.save()
    buf.seek(0)



    #c.drawText(textob)
    #c.showPage()
    #c.save()
    #buf.seek(0)


    return FileResponse(buf, as_attachment=True, filename = asset.Asset_QR + '.pdf')

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
        df['Weight'] = '0'
        df['Ecommerce_Title']= df['Make'] + ' ' + df['Model'] + ' ' + df['CPU'] + ' ' + df['RAM'].astype(str) + 'GB RAM' + df['Storage_Capacity'].astype(str)
        df['Ecommerce_Category']=''
        df['Ecommerce_Condition']=''
        df['Ecommerce_Condition_Description']=''
        df['Ecommerce_Item_Description']=''
        df['Ecommerce_Price']='0'
        df['Ecommerce_SuitableFor']='Casual Computing'
        df['Ecommerce_FormFactor']=''
        df['Ecommerce_Features']=''
        df['Ecommerce_Connectivity']=''
        df['Created'] = date
        df['Updated'] = date

        # CREATING NEW CLEANED UP DATA TABLE
        df = df[
            [
                'Order_Number_id', 'Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                'GPU', 'Motherboard_Test', 'CPU_Test', 'RAM_Test', 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result',
                'Weight', 'Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Condition_Description', 'Ecommerce_Item_Description', 'Ecommerce_Price',
                'Ecommerce_SuitableFor', 'Ecommerce_FormFactor','Ecommerce_Features', 'Ecommerce_Connectivity' ,'Created', 'Updated'
            ]
        ]
        df = df.drop_duplicates(subset='Serial_Number', keep="first") #for some reason pandas sometimes duplicates some of the files, this drops duplicate records
        df.to_sql('SWIPapp_asset',engine, if_exists='append', index=False)
        df.to_csv('final2.csv', index=False)


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
    hdd = HDD.objects.filter(Order_Number_id=order)

    assetcount = Asset.objects.filter(Order_Number_id=order).count
    hddcount = HDD.objects.filter(Order_Number_id=order).count

    context = {'order':order,
                'asset':asset,
                'hdd':hdd,
                'assetcount':assetcount,
                'hddcount':hddcount,
                }

    return render(request, 'SWIPapp/orderindex.html', context)
    


def importassetlshw(request):


    return render(request, 'SWIPapp/importassetlshw.html')


def importassettoorder(request,id):
    order = Order.objects.get(id=id)
    asset = Asset.objects.filter(Order_Number_id=order)
    OrderID = Order.objects.filter(id=id).values('id')[0]['id']
    date = datetime.now()
    hdd = HDD.objects.filter(Order_Number_id=order)
    assetcount = Asset.objects.filter(Order_Number_id=order).count
    hddcount = HDD.objects.filter(Order_Number_id=order).count
    
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
        df['Weight'] = '0'
        df['Ecommerce_Title']= df['Make'] + ' ' + df['Model'] + ' ' + df['CPU']  + ' ' + df['RAM'].astype(str) + 'GB RAM'
        df['Ecommerce_Title'] = df['Ecommerce_Title'].str.replace('.0', '', regex=False)
        df['Ecommerce_Category']=''
        df['Ecommerce_Condition']=''
        df['Ecommerce_Condition_Description']=''
        df['Ecommerce_Item_Description']=''
        df['Ecommerce_Price']='0'
        df['Ecommerce_SuitableFor']='Casual Computing'
        df['Ecommerce_FormFactor']=''
        df['Ecommerce_Features']=''
        df['Ecommerce_Connectivity']=''
        df['Created'] = date
        df['Updated'] = date

        # CREATING NEW CLEANED UP DATA TABLE
        df = df[
            [
                'Order_Number_id', 'Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                'GPU', 'Motherboard_Test', 'CPU_Test', 'RAM_Test', 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result',
                'Weight', 'Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Condition_Description', 'Ecommerce_Item_Description', 'Ecommerce_Price',
                'Ecommerce_SuitableFor', 'Ecommerce_FormFactor','Ecommerce_Features', 'Ecommerce_Connectivity','Created', 'Updated'
            ]
        ]
        df = df.drop_duplicates(subset='Serial_Number', keep="first") #for some reason pandas sometimes duplicates some of the files, this drops duplicate records
        df.to_sql('SWIPapp_asset',engine, if_exists='append', index=False)

        return HttpResponseRedirect("/order/{id}".format(id=id))

    context = {'order':order,
                'asset':asset,
                'hdd':hdd,
                'assetcount':assetcount,
                'hddcount':hddcount,
                }

    return render(request, 'SWIPapp/importassettoorder.html', context)
    
def importhddtoorder(request,id):
    order = Order.objects.get(id=id)
    asset = Asset.objects.filter(Order_Number_id=order)
    OrderID = Order.objects.filter(id=id).values('id')[0]['id']
    date = datetime.now()
    hdd = HDD.objects.filter(Order_Number_id=order)

    assetcount = Asset.objects.filter(Order_Number_id=order).count
    hddcount = HDD.objects.filter(Order_Number_id=order).count

    if request.method == 'POST':
        files=request.FILES.getlist("myfile")
        df = pd.concat(
            map(pd.read_csv, files), ignore_index=True)
        
        engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')

         # RULES TO CLEAN UP THE BASIC INFO
        df['Order_Number_id'] = OrderID
        df['Asset_QR'] = df['user3']

        # RULES TO CLEAN UP STORAGE INFO
        df['Storage'] = df['Vendor'] + ' ' + df['Drive Model']
        df['Storage_Serial_Number'] = df['Drive Serial']

        # RULES TO CLEAN UP THE STORAGE CAPACITY SYNTAX, TURN IT INTO INTEGER AND ROUND UP TO FULL NUMBER
        df[['Storage_Capacity', 'STRx']] = df['Drive Size'].str.split('.', n=1, expand=True)
        df['Storage_Capacity'] = df['Storage_Capacity'].astype(int)
        df['Storage_Capacity'] = df['Storage_Capacity'].div(1024)
        df['Storage_Capacity'] = df['Storage_Capacity'].round(decimals=0)

        df['Wipe_Method'] = df['Wipe Pattern']
        df['Wipe_Start_Time'] = df['Action Start Time']
        df['Wipe_End_Time'] = df['Action End Time']
        df['Wipe_Result'] = df['Action Result']

        # CREATING NEW CLEANED UP DATA TABLE
        df = df[
            [
                'Order_Number_id', 'Asset_QR', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result'
            ]
        ]

        df = df.drop_duplicates(subset='Storage_Serial_Number', keep="first")

        df.to_sql('SWIPapp_hdd',engine, if_exists='append', index=False)

        return HttpResponseRedirect("/order/{id}".format(id=id))

    context = {'order':order,
                'asset':asset,
                'hdd':hdd,
                'assetcount':assetcount,
                'hddcount':hddcount,
                }

    return render(request, 'SWIPapp/importhddtoorder.html', context)

def detachassetfromorder(request,id):
    order = Order.objects.get(id=id)
    asset = Asset.objects.filter(Order_Number_id=order)
    hdd = HDD.objects.filter(Order_Number_id=order)

    context = {'order':order,
                'asset':asset,
                'hdd':hdd,
                }

    return render(request, 'SWIPapp/detachassetfromorder.html', context)

def orderreport(request, id):
    order = Order.objects.get(id=id)
    asset = Asset.objects.filter(Order_Number_id=order)
    hdd = HDD.objects.filter(Order_Number_id=order)

    context = {'order':order,
                'asset':asset,
                'hdd':hdd,
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

    searchterm = asset.Ecommerce_Title
    searchterm.replace(" ", "+")



    url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_TitleDesc=0&LH_BIN=1&LH_ItemCondition=3000&rt=nc&LH_Sold=1&LH_Complete=1&LH_ItemCondition=3000'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')



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

        
    productsdf = productsdf[
            ['Title', 'SoldPrice', 'SoldDate', 'ListingLink']
            ]
        
    productsdf = productsdf.sort_values(by=['SoldPrice'])

    rowcount = productsdf.shape[0]
    todelete = round(0.05*rowcount)
        
    productsdf = productsdf.drop(productsdf.head(todelete).index)
    productsdf = productsdf.drop(productsdf.tail(todelete).index)

    median = productsdf['SoldPrice'].median()

    productsdf.to_csv('output.csv')

    context = {
        'asset':asset,
        'ebayitem': ebayitem,
        'searchterm':searchterm,
        'median':median,
            }

    return render(request, 'SWIPapp/assetindexecommerce.html', context)
   

def assettocsv (request, id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=eBayListing.csv'

    writer = csv.writer(response)
    asset = Asset.objects.get(id=id)
    Cpuclock = asset.CPU.split("@ ")[1]
    RamValue = str(asset.RAM).split(".")[0] + " GB"
    StorageCapacity = str(asset.Storage_Capacity).split(".")[0] + " GB"

    #index row
    writer.writerow(['*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193|CC=UTF-8)','CustomLabel', '*Category', 'StoreCategory', '*Title', 'Subtitle','Relationship', 'RelationshipDetails', '*ConditionID', 'VAT%', '*C:Brand', '*C:Type', '*C:Series', '*C:RAM Size', '*C:Processor', '*C:Hard Drive Capacity', '*C:Storage Type', '*C:Form Factor', '*C:GPU', '*C:Operating System',
    '*C:Processor Speed', '*C:Most Suitable For', '*C:Screen Size', '*C:Connectivity', '*C:Features', '*C:Model', '*C:MPN', '*C:Unit Quantity', '*C:Unit Type', '*C:Release Year', '*C:SSD Capacity', 'C:Maximum RAM Capacity', '*C:Colour', 'C:Graphics Processing Type', 'C:Country/Region of Manufacture', 'C:Manufacturer Warranty', 'C:Custom Bundle',
    'C:Bundle Description', 'C:Item Height', 'C:Item Length', 'C:Item Width', 'C:Motherboard Model', '*C:Maximum Resolution', 'C:Item Weight', 'PicURL', 'GalleryType', '*Description', '*Format', '*Duration', '*ListingDuration', '*StartPrice', '*Quantity', 'PayPalAccepted', 'PayPalEmailAddress', 'ImmediatePayRequired', 'PaymentInstructions',
    '*Location', 'ShippingType', 'ShippingService-1:Option', 'ShippingService-1:Cost', 'ShippingService-2:Option', 'ShippingService-2:Cost', '*DispatchTimeMax', 'PromotionalShippingDiscount', 'ShippingDiscountProfileID', 'DomesticRateTable', '*ReturnsAcceptedOption', 'ReturnsWithinOption', 'RefundOption', 'ShippingCostPaidByOption',
    'AdditionalDetails', 'TakeBackPolicyID', 'ProductCompliancePolicyID'])
    
    #info row
    writer.writerow(['Add', asset.Asset_QR, asset.Ecommerce_Category, '', asset.Ecommerce_Title, '', '', '', asset.Ecommerce_Condition, '20', asset.Make, asset.Type, asset.Model, RamValue, asset.CPU, StorageCapacity, asset.Storage_Type, asset.Type, asset.GPU, asset.Operating_System, Cpuclock, asset.Ecommerce_SuitableFor, asset.Screen_Size, asset.Ecommerce_Connectivity, asset.Ecommerce_Features,
    asset.Model, asset.Model,'1', 'Unit', 'N/A', StorageCapacity, 'N/A', '', '', '', 'None', 'No', '', '', '', '', '', asset.Screen_Resolution, asset.Weight, 'https://i.imgur.com/jTHazme.jpg', '', 'Description', 'FixedPrice', 'GTC','GTC', asset.Ecommerce_Price, '1', '', '', '1', '', 'NW10 6HJ', '', 'UK_OtherCourier3Days', '0', '', '', '2', '', '', '', 'Days_30', '', '', '', '', '', ''])

    return response


def assetecommerceedit (request, id):
    asset = Asset.objects.get(id=id)
    form = AssetEcommerce(instance=asset)

    if request.method == 'POST':
        form = AssetEcommerce(request.POST, instance=asset)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect("/asset/{id}/ecommerce".format(id=id))

    context = {
        'form':form,
        'asset':asset
    }

    return render(request, 'SWIPapp/assetecommerceedit.html', context)

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

    context = {
        'asset':asset,
        'form':form}
    return render(request, 'SWIPapp/updateasset.html', context)

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
    asset = Lists.objects.get(id=id).AttachedAssets.filter




    context = {
        'list':list,
        'asset':asset
    }

    return render (request, 'SWIPapp/listindex.html', context)


def webscraper (request):
    
    context = {}

    return render (request, 'SWIPapp/webscraper.html', context)