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
            'Make': forms.TextInput(attrs={'class': 'assetmake', 'placeholder ': 'Asset Make'}),
            'Model': forms.TextInput(attrs={'class': 'assetmodel', 'placeholder ': 'Asset Model'}),
            'Serial_Number': forms.TextInput(attrs={'class': 'assetserial', 'placeholder ': 'Asset Serial Number'}),
            'CPU': forms.TextInput(attrs={'class': 'assetcpu', 'placeholder ': 'Processor Make, Model and Clock'}),
            'RAM': forms.TextInput(attrs={'class': 'assetram', 'placeholder ': 'RAM Memory Amount'}),
            'Storage': forms.TextInput(attrs={'class': 'assetstorage', 'placeholder ': 'Storage Make and Model'}),
            'Storage_Serial_Number': forms.TextInput(attrs={'class': 'assetstorageserial', 'placeholder ': 'Storage Serial Number'}),
            'Storage_Capacity': forms.TextInput(attrs={'class': 'assetstoragecap', 'placeholder ': 'Storage Capacity'}),
            'GPU': forms.TextInput(attrs={'class': 'assetgpu', 'placeholder ': 'GPU Info'}),
            'Weight': forms.TextInput(attrs={'class': 'assetweight', 'placeholder ': 'Weight'}),
        }


ConditionCodes = [
    ('2750 - Like New', '2750 - Like New'),
    ('3000 - Used', '3000 - Used'),
    ('4000 - Very Good', '4000 - Very Good'),
    ('5000 - Good', '5000 - Good'),
    ('6000 - Acceptable', '6000 - Acceptable'),
    ('7000 - For Parts Not Working', '7000 - For parts not working'),
    ]

CategoryCodes = [
    ('111418 - Apple Desktop', '111418 - Apple Desktop/iMac'),
    ('179 - PC Desktop/AIO', '179 - PC Desktop/AIO'),
    ('111422 - Apple Laptop', '111422 - Apple Laptop'),
    ('177 - PC Laptop', '177 - PC Laptop')
    ]

ItemTypes = [
    ('All-in-One', 'All-in-One'),
    ('Desktop', 'Desktop'),
    ('Laptop/Notebook', 'Laptop/Notebook'),
]

OperatingSystems = [
    ('Windows 10', 'Windows 10'),
    ('Windows 10 Pro', 'Windows 10 Pro'),
    ('Windows 10 Home', 'Windows 10 Home'),
    ('Windows 11', 'Windows 11'),
    ('Mac OS 10.11 El Capitan', 'Mac OS 10.11 El Capitan'),
    ('Mac OS 10.12 Sierra', 'Mac OS 10.12 Sierra'),
    ('Mac OS 10.13 High Sierra', 'Mac OS 10.13 High Sierra'),
    ('Mac OS 10.14 Mojave', 'Mac OS 10.14 Mojave'),
    ('Mac OS 10.15 Catalina', 'Mac OS 10.15 Catalina'),
    ('Mac OS 11 Big Sur', 'Mac OS 11 Big Sur'),
    ('Mac OS 12 Monterey', 'Mac OS 12 Monterey'),
    ('Mac OS 13 Ventura', 'Mac OS 13 Ventura'),
]

class AssetEcommerce(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Price', 'Type', 'Operating_System',)

        widgets = {
            'Ecommerce_Title': forms.TextInput(attrs={'class': 'ecommercetitle', 'placeholder ': 'eBay Title'}),
            'Ecommerce_Category': forms.Select(choices=CategoryCodes, attrs={'class':'conditionselect'}),
            'Ecommerce_Condition': forms.Select(choices=ConditionCodes, attrs={'class':'conditionselect'}),
            'Ecommerce_Price': forms.TextInput(attrs={'class': 'ecommerceprice', 'placeholder ': 'Price'}),
            'Type': forms.Select(choices=ItemTypes, attrs={'class':'conditionselect'}),
            'Operating_System': forms.Select(choices=OperatingSystems, attrs={'class':'conditionselect'}),
         }

class CreateNewList(forms.ModelForm):
    class Meta:
        model = Lists
        fields = ('ListName', )
    
        widgets = {
            'ListName': forms.TextInput(attrs={'class': 'ListName', 'placeholder': 'Name Your List'}),
    }