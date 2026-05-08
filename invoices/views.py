from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Invoice, Client, Item
from  .forms import GuestInvoiceForm, ClientInvoiceForm,ItemFormSet
from datetime import  date
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint,os
from weasyprint import HTML
from datetime import date,datetime
from django.shortcuts import render, redirect
from .models import Invoice, Item
from .forms import GuestInvoiceForm, ItemFormSet,CreateClientForm


@login_required
def invoice_list(request):
    if request.user.is_staff or request.user.is_superuser:
        invoices = Invoice.objects.all()
    else:
        invoices = Invoice.objects.filter(created_by=request.user)
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})



def guest_invoice_create(request):
    current_year = date.today().year

    # Calculate the next invoice number for the current year
    last_invoice = Invoice.objects.filter(year=current_year).order_by('-invoice_no').first()
    if last_invoice:
        next_invoice_no = last_invoice.invoice_no + 1
    else:
        next_invoice_no = 1

    # Optional: default suffix (currently not used)
    default_suffix = 'A'

    # Full invoice number display
    #preview_invoice_no = f"{current_year}-{str(next_invoice_no).zfill(3)}-{default_suffix}"
    preview_invoice_no = next_invoice_no

    if request.method == 'POST':
        # Bind the form and items
        form = GuestInvoiceForm(request.POST)
        formset = ItemFormSet(request.POST)

        # Debugging: show why forms might be invalid
        print("Form is valid?", form.is_valid())
        print("Form errors:", form.errors)
        print("Formset is valid?", formset.is_valid())
        print("Formset errors:", formset.errors)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = None  # guest invoice, no user
            #invoice.suffix = 'A'  # optional
            invoice.year = current_year
            invoice.invoice_no = next_invoice_no
            invoice.save()  # invoice_no assigned and invoice saved


            total = 0
            # Save items
            items = formset.save(commit=False)
            for item in items:
                item.invoice = invoice
                item.save()
                total += item.total
            
            # Update total on invoice
            invoice.total = total
            
            # Adjust due date logic based on status
            # Already handled in model.save(), so this is optional
            if invoice.status in ['paid_upfront', 'already_paid', 'due_paid']:
                invoice.due_date = None
            invoice.save()

            # if request.headers.get('HX-Request'):
            #     # Redirect to the detail page, but tell HTMX to only pick the content
            #     response = redirect('invoice_detail', pk=invoice.pk)
            #     # We can use a custom header to tell the frontend to stay in the dashboard
            #     return response
            
            # Redirect to a "success page" or invoice detail page
            return redirect('invoice_detail', pk=invoice.id)
    
    else:
        form = GuestInvoiceForm()
        formset = ItemFormSet()

    return render(request, 'invoices/guest_invoice_create.html', {
        'form': form,
        'formset': formset,
        'preview_invoice_no': preview_invoice_no
    })

@login_required
def client_invoice_create(request):
    if request.method == 'POST':
        form = ClientInvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            return redirect('invoice_detail', invoice.id)
    else:
        form = ClientInvoiceForm()
    return render(request, 'invoices/client_invoice_create.html', {'form': form})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if not (invoice.created_by == request.user or request.user.is_staff or request.user.is_superuser):
        return HttpResponse("You are not authorized to view this invoice.", status=403)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    logo_path = os.path.join(settings.MEDIA_ROOT, 'defaultlogo.png')
    if not (invoice.created_by == request.user or request.user.is_staff or request.user.is_superuser):
        return HttpResponse("You are not authorized to view this invoice.", status=403)
    html_string = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice, "logo_url": f"{request.scheme}://{request.get_host()}/media/uploads/defaultlogo.png"})
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{invoice.id}.pdf'
    return response
    #return render(request, "invoices/invoice_pdf.html",{'invoice': invoice, "logo_url": f"{request.scheme}://{request.get_host()}/media/uploads/defaultlogo.png"})



@login_required
def create_new_client(request):
    if request.method == 'POST':
        form = CreateClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect("client_invoice_create")
    else:
        form = CreateClientForm()
    return render(request, 'invoices/client_create.html', {'form': form})

@login_required
def dashboard(request):
    total_invoice = Invoice.objects.filter(date__year=datetime.now().year).count()
    pending_invo_count = Invoice.objects.filter(status__in=['payment_due', 'partially_paid', 'due_paid']).count()
    print(pending_invo_count)
    return render(request, 'invoices/dashboard.html', {'invoice_count':total_invoice,'pending_count':pending_invo_count})
