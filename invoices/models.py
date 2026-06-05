from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid 
from django.core.validators import MinValueValidator
def current_year():
    from datetime import date
    return date.today().year

class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    place = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

class Firm(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    place = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class InvoiceLabel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_label_title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

class InvoiceLabel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_label_title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

class InvoiceTheme(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    theme_name = models.CharField(max_length=200)
    theme_config = models.JSONField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('payment_due', 'Payment After Service'),
        ('partially_paid', 'Partially Paid'),
        ('due_paid', 'Previously Due, Now Paid'),
    ]
    special_uid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False
    )
    image = models.ImageField(
        upload_to='',
        blank=True,          
        null=True            
    )
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
    
    invoice_label =models.ForeignKey(InvoiceLabel, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(Firm, on_delete=models.SET_NULL, null=True, blank=True)
    theme_style = models.ForeignKey(InvoiceTheme, on_delete=models.SET_NULL, null=True, blank=True)
    context_title = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Specific subject (e.g., Machine Name, Project Code, or Service Type)"
    )

    # Updated Alignment Choices
    LABEL_ALIGNMENT = [
        ('LEFT', 'Left Aligned'),
        ('CENTER', 'Centered'),
        ('RIGHT', 'Right Aligned'),
    ]
    
    header_style = models.CharField(
        max_length=10, 
        choices=LABEL_ALIGNMENT, 
        default='CENTER'  # Now defaults to Center
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True,
        null=True, 
        editable=True # Set to False if you want to hide it from the Admin form
    )
    is_active = models.BooleanField(default=True)

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
        if self.status in ['paid',  'due_paid']:
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


    # def __str__(self):
    #     if self.client:
    #         return f"Invoice {self.id} for {self.client.name}"
    #     return f"Invoice {self.id} for {self.guest_client_name}"

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    @property
    def total(self):
        return self.quantity * self.price


class DiscountCategory(models.Model):
    """
    Real table for firms to manage categories (e.g., 'Black Friday').
    """
    SYSTEM_TYPE_CHOICES = [
        ('SEASONAL', 'Seasonal / Festival Campaign'),
        ('COUPON', 'Promo / Coupon Code'),
        ('LOYALTY', 'Loyalty / Reward Points'),
        ('VOLUME', 'Bulk / Volume Discount'),
        ('CUSTOM', 'Other / Custom Offer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE, related_name="discount_categories")
    name = models.CharField(max_length=50)
    system_type = models.CharField(
        max_length=20, 
        choices=SYSTEM_TYPE_CHOICES, 
        default='CUSTOM',
        help_text="Underlying core category behavior"
    )
    code = models.CharField(max_length=50, blank=True, null=True, help_text="Coupon code if applicable")

    def __str__(self):
        return f"{self.name} [{self.get_system_type_display()}] ({self.firm.name})"


class Discount(models.Model):
    """
    Reusable discount rule configurations created by firm admins.
    Can be completely hard-deleted later to save space.
    """
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage Based (%)'),
        ('FLAT', 'Flat Amount Deduction ($)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(DiscountCategory, on_delete=models.SET_NULL, null=True, related_name="discounts_category")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, related_name="discounts_category")
    
    name = models.CharField(max_length=100, help_text="e.g., Black Friday 20% Off")
    applied_code = models.CharField(max_length=50, blank=True, null=True, help_text="Coupon code if applicable")
    
    # Crucial: Calculation type is kept right here alongside the math configuration
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='PERCENTAGE')
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])


    def __str__(self):
        return f"{self.name} ({self.get_discount_type_display()})"
