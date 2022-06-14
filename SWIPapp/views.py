from django.shortcuts import render, redirect
from .models import Order, Asset
from django.http import HttpResponse
from .forms import CreateNewOrder



# Create your views here.

# THIS IS THE HOME PAGE - DISPLAYS SEARCH + LIST OF RECENTLY CREATED AND EDITED ASSETS:
def navbar(request):
    return render (request, 'SWIPsite/navbar.html')

def home(request):
    return render (request, 'SWIPapp/home.html')

def assets(request):
    asset = Asset.objects.all()

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