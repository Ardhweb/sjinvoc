from django import forms
from .models import Invoice, Client

from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, Item

class GuestInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['guest_client_name', 'due_date', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guest_client_name': forms.TextInput(attrs={'class': 'form-control'})
        }

ItemFormSet = inlineformset_factory(
    Invoice,
    Item,
    fields=['item_name', 'quantity', 'price'],
    extra=1,
    can_delete=True,
    widgets={
        'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Pilot Line Filter 0018A'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'value':1}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'value':0, 'step':0.01})
    }
)

class ClientInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'due_date']