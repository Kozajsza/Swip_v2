from tkinter import Widget
from django import forms
from .models import Order

class CreateNewOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('Order_Number', 'Customer', 'Customer_Address')

        widgets = {
            'Order_Number': forms.TextInput(attrs={'class': 'ordernumber', 'placeholder ': 'Order Number'}),
            'Customer': forms.TextInput(attrs={'class': 'ordercustomer', 'placeholder ': 'Customer Name'}),
            'Customer_Address': forms.TextInput(attrs={'class': 'orderaddress', 'placeholder ': 'Full Address including Postcode'}),
        }
