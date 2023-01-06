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
    ('2750', '2750 - Like New'),
    ('3000', '3000 - Used'),
    ('4000', '4000 - Very Good'),
    ('5000', '5000 - Good'),
    ('6000', '6000 - Acceptable'),
    ('7000', '7000 - For parts not working'),
    ]

CategoryCodes = [
    ('111418', '111418 - Apple Desktop/iMac'),
    ('179', '179 - PC Desktop/AIO'),
    ('111422', '111422 - Apple Laptop'),
    ('177', '177 - PC Laptop')
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

ScreenSize = [
    ('11in', '11in'),
    ('13in', '13in'),
    ('14in', '14in'),
    ('15in', '15in'),
    ('17in', '17in'),
    ('21in', '21in'),
    ('24in', '24in'),
    ('27in', '27in'),
]

ScreenResolution = [
    ('1280x720', '1280x720'),
    ('1366x768', '1366x768'),
    ('1600x900', '1600x900'),
    ('1920x1080', '1920x1080'),
    ('2560x1440', '2560x1440'),
    ('3840x2160', '3840x2160'),
]

SuitableFor = [
    ('Casual Computing', 'Casual Computing'),
    ('Gaming', 'Gaming'),
    ('Office', 'Office'),
    ('Workstation', 'Workstation'),
    ('Graphic Design', 'Graphic Design'),
]

Connectivity = [
    ('USB 2.0', 'USB 2.0'),
    ('USB 3.0', 'USB 3.0'),
    ('USB-C', 'USB-C'),
    ('VGA', 'VGA'),
    ('HDMI', 'HDMI'),
    ('Display-Port', 'Display-Port'),
    ('DVI', 'DVI'),
    ('DVI-D', 'DVI-D'),
]

Features =[
    ('Backlit Keyboard', 'Backlit Keyboard'),
    ('Bluetooth', 'Bluetooth'),
    ('Built-in Microphone', 'Built-in Microphone'),
    ('Built-in Camera', 'Built-in Camera'),
    ('Touchscreen', 'Touchscreen'),
    ('Wi-Fi', 'Wi-Fi'),
    ('Memory Card(s) Reader', 'Memory Card(s) Reader'),
    ('SD Card Slot', 'SD Card Slot'),
    ('Touch ID', 'Touch ID'),
]

class AssetEcommerce(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('Ecommerce_Title', 'Ecommerce_Category', 'Ecommerce_Condition', 'Ecommerce_Price', 'Type', 'Operating_System', 'Screen_Size', 'Screen_Resolution', 'Ecommerce_SuitableFor', 'Ecommerce_Connectivity','Ecommerce_Features',)

        widgets = {
            'Ecommerce_Title': forms.TextInput(attrs={'class': 'ecommercetitle', 'placeholder ': 'eBay Title'}),
            'Ecommerce_Category': forms.Select(choices=CategoryCodes, attrs={'class':'conditionselect'}),
            'Ecommerce_Condition': forms.Select(choices=ConditionCodes, attrs={'class':'conditionselect'}),
            'Ecommerce_Price': forms.TextInput(attrs={'class': 'ecommerceprice', 'placeholder ': 'Price'}),
            'Type': forms.Select(choices=ItemTypes, attrs={'class':'conditionselect'}),
            'Operating_System': forms.Select(choices=OperatingSystems, attrs={'class':'conditionselect'}),
            'Screen_Size': forms.Select(choices=ScreenSize, attrs={'class':'conditionselect'}),
            'Screen_Resolution': forms.Select(choices=ScreenResolution, attrs={'class':'conditionselect'}),
            'Ecommerce_SuitableFor': forms.CheckboxSelectMultiple(choices=SuitableFor),
            'Ecommerce_Connectivity': forms.CheckboxSelectMultiple(choices=Connectivity),
            'Ecommerce_Features': forms.CheckboxSelectMultiple(choices=Features),
         }

class CreateNewList(forms.ModelForm):
    class Meta:
        model = Lists
        fields = ('ListName', )
    
        widgets = {
            'ListName': forms.TextInput(attrs={'class': 'ListName', 'placeholder': 'Name Your List'}),
    }