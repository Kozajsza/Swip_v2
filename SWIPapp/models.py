from django.db import models
from io import BytesIO
from django.core.files import File
import qrcode  
from PIL import Image, ImageDraw

# Create your models here.


class Order(models.Model):
    Order_Number = models.CharField(max_length=100)
    Customer = models.CharField(max_length=100, default='')
    Customer_Address = models.TextField(max_length=300, default='')
    Created = models.DateTimeField(auto_now_add=True) #this is currently broken - works on import but updating returns error if null=False for some reason
    Updated = models.DateTimeField(auto_now_add=True) #this is currently broken - works on import but updating returns error if null=False for some reason

    class Meta:
        ordering =['-Updated', '-Created']

    def __str__(self):
        return self.Order_Number

ConditionCodes = [
    ('2750 - Like New', '2750 - Like New'),
    ('3000 - Used', '3000 - Used'),
    ('4000 - Very Good', '4000 - Very Good'),
    ('5000 - Good', '5000 - Good'),
    ('6000 - Acceptable', '6000 - Acceptable'),
    ('7000 - For parts not working', '7000 - For parts not working'),
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

class Asset(models.Model):
    Order_Number = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    Asset_QR = models.CharField(max_length=100, default='')
    Asset_QR_Img = models.ImageField (upload_to='SWIPapp\static\SWIPapp\images\qr_codes', blank=True, null=True)
    Type = models.CharField(max_length=100, default='', null=True, blank=True)
    Make = models.CharField(max_length=100, default='',null=True, blank=True)
    Model = models.CharField(max_length=100, default='',null=True, blank=True)
    Serial_Number = models.CharField(max_length=100, default='',null=True, blank=True)
    CPU = models.CharField(max_length=100, default='',null=True, blank=True)
    RAM = models.FloatField(null=True, blank=True)
    Storage = models.CharField(max_length=100, default='',null=True, blank=True)
    Storage_Serial_Number = models.CharField(max_length=100, default='',null=True, blank=True)
    Storage_Capacity = models.FloatField(null=True, blank=True)
    Storage_Type = models.CharField(max_length=100, default='',null=True, blank=True)
    GPU = models.CharField(max_length=100, default='',null=True, blank=True)
    Motherboard_Test = models.CharField(max_length=100, default='',null=True, blank=True)
    CPU_Test = models.CharField(max_length=100, default='',null=True, blank=True)
    RAM_Test = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_Method = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_Start_Time = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_End_Time = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_Result = models.CharField(max_length=100, default='',null=True, blank=True)
    Weight = models.FloatField(null=True, blank=True, default='0')
    Operating_System = models.CharField(max_length=100, default='Not Installed',null=True, blank=True)
    Screen_Size = models.CharField(max_length=10, default='N/A',null=True, blank=True)
    Screen_Resolution = models.CharField(max_length=10, default='N/A',null=True, blank=True)
    Ecommerce_Title = models.CharField(max_length=80, default='', null=True, blank=True)
    Ecommerce_Category = models.CharField(max_length=35, default='', null=True, blank=True)
    Ecommerce_Condition = models.CharField(max_length=20, default='', null=True, blank=True)
    Ecommerce_Condition_Description = models.CharField(max_length=1000, default='', null=True, blank=True)
    Ecommerce_Item_Description = models.CharField(max_length=1000, default='', null=True, blank=True)
    Ecommerce_Price = models.FloatField(null=True, blank=True, default='0')
    Ecommerce_SuitableFor = models.CharField(max_length=200, default='', null=True, blank=True)
    Ecommerce_FormFactor = models.CharField(max_length=35, default='', null=True, blank=True)
    Ecommerce_Features = models.CharField(max_length=200, default='', null=True, blank=True)
    Ecommerce_Connectivity = models.CharField(max_length=200, default='', null=True, blank=True)
    Created = models.DateTimeField(auto_now_add=True, null=True) #this is currently broken - works on import but updating returns error if null=False for some reason
    Updated = models.DateTimeField(auto_now_add=True, null= True) #this is currently broken - works on import but updating returns error if null=False for some reason


    def __str__(self):
        return self.Asset_QR

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.Asset_QR)
        canvas = Image.new('RGB', (290,290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'{self.Asset_QR}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.Asset_QR_Img.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

class AssetLog(models.Model):
    ConnectedAsset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True)
    Log = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.Log

class ebayLookup(models.Model):
    ConnectedAsset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True)
    Title = models.CharField(max_length=100, default='')
    SoldPrice = models.FloatField(null=True, blank=True)
    SoldDate = models.CharField(max_length=100, default='')
    ListingLink = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.Title


class HDD(models.Model):
    Order_Number = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    Asset_QR = models.CharField(max_length=100, default='')
    Asset_QR_Img = models.ImageField (upload_to='main\static\lessapp\images\qr_codes', blank=True, null=True)
    Storage = models.CharField(max_length=100, default='',null=True, blank=True)
    Storage_Serial_Number = models.CharField(max_length=100, default='',null=True, blank=True)
    Storage_Capacity = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_Method = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_Start_Time = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_End_Time = models.CharField(max_length=100, default='',null=True, blank=True)
    Wipe_Result = models.CharField(max_length=100, default='',null=True, blank=True)
    Created = models.DateTimeField(auto_now_add=True, null=True) #this is currently broken - works on import but updating returns error if null=False for some reason
    Updated = models.DateTimeField(auto_now_add=True, null= True) #this is currently broken - works on import but updating returns error if null=False for some reason


    class Meta:
        ordering =['-Updated', '-Created']

    def __str__(self):
        return self.Asset_QR


class Lists(models.Model):
    ListName = models.CharField(max_length=100, default='')
    AttachedAssets = models.ManyToManyField(Asset)
    Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-Created']