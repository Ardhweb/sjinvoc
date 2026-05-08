from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from datetime import date
def current_year():
    from datetime import date
    return date.today().year

class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    place = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('paid_upfront', 'Paid Upfront (No Due)'),
        ('payment_due', 'Payment After Service (Due Date Required)'),
        ('partially_paid', 'Partially Paid (Due Date Required)'),
        ('already_paid', 'Already Paid (No Due)'),
        ('due_paid', 'Previously Due, Now Paid (No Due)'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    guest_client_name = models.CharField(max_length=200, blank=True)  # For guest invoices
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='payment_due')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    place = models.CharField(max_length=20, blank=True, null=True)
    # New fields for invoice numbering
    invoice_no = models.PositiveIntegerField(null=True, blank=True, editable=False)
    year = models.PositiveIntegerField(default=current_year, editable=False)
    suffix = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Handle invoice_no auto-increment per year
        if not self.invoice_no:
            current_year = date.today().year
            self.year = current_year
            last_invoice = Invoice.objects.filter(year=current_year).order_by('-invoice_no').first()
            if last_invoice:
                self.invoice_no = last_invoice.invoice_no + 1
            else:
                self.invoice_no = 1  # first invoice of the year

        # Handle due_date logic
        if self.status in ['paid_upfront', 'already_paid', 'due_paid']:
            self.due_date = None
        super().save(*args, **kwargs)

    # @property
    # def full_invoice_no(self):
    #     # Format: YEAR-INVOICE_NO-SUFFIX (example: 2026-001-A)
    #     no = str(self.invoice_no).zfill(3)  # 001, 002, etc.
    #     if self.suffix:
    #         return f"{self.year}-{no}-{self.suffix}"
    #     return f"{self.year}-{no}"

    @property
    def full_invoice_no(self):
        return str(self.invoice_no)


    def __str__(self):
        if self.client:
            return f"Invoice {self.id} for {self.client.name}"
        return f"Invoice {self.id} for {self.guest_client_name}"

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.price