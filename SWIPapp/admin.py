from django.contrib import admin
from .models import Order, Asset, AssetLog, ebayLookup, Lists

# Register your models here.

admin.site.register(Order)
admin.site.register(Asset)
admin.site.register(AssetLog)
admin.site.register(ebayLookup)
admin.site.register(Lists)