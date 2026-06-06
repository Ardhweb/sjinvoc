from django import forms
from .models import Invoice, Client
from django import forms
from django.forms import inlineformset_factory,models
from .models import Invoice, Item, Client, Discount

class GuestInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['guest_client_name', 'due_date', 'status', 'context_title']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control form-select','aria-label':"Default select example"}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guest_client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'context_title': forms.TextInput(attrs={'class': 'form-control'}),
            #'header_style': forms.Select(attrs={'class': 'form-control'}),
        }

# class BaseItemFormSet(models.BaseInlineFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Only show items where is_active is True
#         self.queryset = self.instance.items.filter(is_active=True)

ItemFormSet = inlineformset_factory(
    Invoice,
    Item,
    #formset=BaseItemFormSet,
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
        fields = ['client', 'due_date', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control, form-select', 'aria-label':"Default select example"}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # store label class in field for template use
            field.label_suffix = ''  # optional: remove colon
            #field.widget.attrs['label_class'] = 'fw-semibold'
            field.label_class = 'fw-semibold'


class EditInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['guest_client_name','client', 'due_date', 'status']
        widgets = {
            'guest_client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control form-select', 'aria-label':"Default select example"}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # store label class in field for template use
            field.label_suffix = ''  # optional: remove colon
            #field.widget.attrs['label_class'] = 'fw-semibold'
            field.label_class = 'fw-semibold'
class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'place', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Customer Address'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['value', 'discount_type']
        labels = {
            'value': 'Discount',
        }

        widgets = {
        'discount_type': forms.Select(attrs={'class': 'form-control form-select', 'aria-label':"Default select example"}),
        'value': forms.TextInput(attrs={'class': 'form-control',}),  
            
        }
        
