from django.contrib import admin

# Register your models here.
from .models import Invoice, Item,Client 

admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(Client)