from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('navbar',views.navbar, name='navbar'),
    path('assets',views.assets, name='assets'),
    path('orders',views.orders, name='orders'),
    path('order/<int:id>/', views.orderindex, name='orderindex'),
]