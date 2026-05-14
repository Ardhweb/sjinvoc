from django.contrib import admin
import csv
# Register your models here.
from .models import Invoice, Item,Client,InvoiceLabel,InvoiceTheme,Firm
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)  # write header
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected to CSV"

class InvoiceAdmin(admin.ModelAdmin):
	actions=[export_as_csv]

class ClientAdmin(admin.ModelAdmin):
	actions=[export_as_csv]

class ItemAdmin(admin.ModelAdmin):
	actions=[export_as_csv]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(InvoiceTheme)
admin.site.register(Firm)