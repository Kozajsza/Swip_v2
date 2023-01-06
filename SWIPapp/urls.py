from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('navbar',views.navbar, name='navbar'),
    path('login',views.login, name='login'),
    path('assets',views.assets, name='assets'),
    path('orders',views.orders, name='orders'),
    path('order/<int:id>/', views.orderindex, name='orderindex'),
    path('orderreport/<int:id>',views.orderreport, name='orderreport'),
    path('updateorder/<str:id>/', views.updateorder, name="updateorder"),
    path('deleteorder/<str:id>/', views.deleteorder, name="deleteorder"),
    path('importassettoorder/<str:id>/', views.importassettoorder, name='importassettoorder'),
    path('importhddtoorder/<str:id>/', views.importhddtoorder, name='importhddtoorder'),
    path('detachassetfromorder/<str:id>', views.detachassetfromorder, name='detachassetfromorder'),
    path('asset/<int:id>/', views.assetindex, name='assetindex'),
    path('asset/<int:id>/ecommerce', views.assetindexecommerce, name='assetindexecommerce'),
    path('asset/<int:id>/ecommerce/assettocsv', views.assettocsv, name='assettocsv'),
    path('asset/<str:id>/ecommerceedit', views.assetecommerceedit, name='assetecommerceedit'),
    path('assetlabel/<int:id>/', views.assetlabel, name='assetlabel'),
    path('createasset', views.createasset, name='createasset'),
    path('updateasset/<str:id>/', views.updateasset, name="updateasset"),
    path('deleteasset/<str:id>/', views.deleteasset, name="deleteasset"),
    path('lists', views.lists, name='lists'),
    path('list/<int:id>/', views.listindex, name='listindex'),
]