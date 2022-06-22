from django.shortcuts import render, redirect
from .models import Order, Asset
from django.http import HttpResponse
from .forms import CreateNewOrder
import sqlalchemy
import pandas as pd


# Create your views here.

# THIS IS THE HOME PAGE - DISPLAYS SEARCH + LIST OF RECENTLY CREATED AND EDITED ASSETS:
def navbar(request):
    return render (request, 'SWIPsite/navbar.html')

def home(request):
    return render (request, 'SWIPapp/home.html')

def assets(request):
    asset = Asset.objects.all()
    if request.method == 'POST':
        file= request.FILES["myfile"]
        engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')
        df = pd.read_csv(file)
         # RULES TO CLEAN UP THE BASIC INFO
        df['Order_Number_id'] = df['user4']
        df['Asset_QR'] = df['user3']
        df['Type'] = ''
        df['Make'] = df['Computer Vendor']
        df['Model'] = df['Computer Model']
        df['Serial_Number'] = df['Computer Serial']

            # RULES TO CLEAN UP CPU SYNTAX
        df[['CPU', 'CPUx']] = df['CPU 1'].str.split(',', n=1, expand=True)
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
        df['Ecommerce_Title']=''
        df['Ecommerce_Category']=''
        df['Ecommerce_Condition']=''
        df['Ecommerce_Condition_Description']=''
        df['Ecommerce_Item_Description']=''
        df['Ecommerce_Price']=''

        # CREATING NEW CLEANED UP DATA TABLE
        df = df[
            [
                'Order_Number_id', 'Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity',
                'GPU', 'Motherboard_Test', 'CPU_Test', 'RAM_Test', 'Wipe_Method', 'Wipe_Start_Time', 'Wipe_End_Time', 'Wipe_Result',
                'Weight', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Condition_Description', 'Ecommerce_Item_Description', 'Ecommerce_Price'
            ]
        ]
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
    #assets = Asset.objects.filter(Order_Number_id=order)
    #hdds = HDD.objects.filter(Order_Number_id=order)

    context = {'order':order,
                #'assets':assets,
                #'hdds':hdds,
                }

    return render(request, 'SWIPapp/orderindex.html', context)