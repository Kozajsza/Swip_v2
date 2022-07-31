from tkinter import Widget
from django import forms
from .models import Order, AssetLog, Asset, Lists

class CreateNewOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('Order_Number', 'Customer', 'Customer_Address')

        widgets = {
            'Order_Number': forms.TextInput(attrs={'class': 'ordernumber', 'placeholder ': 'Order Number'}),
            'Customer': forms.TextInput(attrs={'class': 'ordercustomer', 'placeholder ': 'Customer Name'}),
            'Customer_Address': forms.TextInput(attrs={'class': 'orderaddress', 'placeholder ': 'Full Address including Postcode'}),
        }

class CreateNewLog(forms.ModelForm):
    class Meta:
        model = AssetLog
        fields = ('Log',)
    
    widgets = {
        'Log': forms.TextInput(attrs={'class': 'LogInput', 'placeholder ': 'Input Log Change'}),
    }



class CreateNewAsset(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('Asset_QR', 'Type', 'Make', 'Model', 'Serial_Number', 'CPU', 'RAM', 'Storage', 'Storage_Serial_Number', 'Storage_Capacity', 'GPU', 'Weight')

        widgets = {
            'Asset_QR': forms.TextInput(attrs={'class': 'assetqr', 'placeholder ': 'Asset Unique QR Code'}),
            'Type': forms.TextInput(attrs={'class': 'assettype', 'placeholder ': 'Asset Type'}),
            'Make': forms.TextInput(attrs={'class': 'assetmake', 'placeholder ': 'Asset Make'}),
            'Model': forms.TextInput(attrs={'class': 'assetmodel', 'placeholder ': 'Asset Model'}),
            'Serial_Number': forms.TextInput(attrs={'class': 'assetserial', 'placeholder ': 'Asset Serial Number'}),
            'CPU': forms.TextInput(attrs={'class': 'assetcpu', 'placeholder ': 'Processor Make, Model and Clock'}),
            'RAM': forms.TextInput(attrs={'class': 'assetram', 'placeholder ': 'RAM Memory Amount'}),
            'Storage': forms.TextInput(attrs={'class': 'assetstorage', 'placeholder ': 'Storage Make and Model'}),
            'Storage_Serial_Number': forms.TextInput(attrs={'class': 'assetstorageserial', 'placeholder ': 'Storage Serial Number'}),
            'Storage_Capacity': forms.TextInput(attrs={'class': 'assetstoragecap', 'placeholder ': 'Storage Capacity'}),
            'Weight': forms.TextInput(attrs={'class': 'assetweight', 'placeholder ': 'Weight in Grams'}),
        }

class CreateNewList(forms.ModelForm):
    class Meta:
        model = Lists
        fields = ('ListName', )
    
        widgets = {
            'ListName': forms.TextInput(attrs={'class': 'ListName', 'placeholder': 'Name Your List'}),
    }