from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('guest/create/', views.guest_invoice_create, name='guest_invoice_create'),
    path('client/create/', views.client_invoice_create, name='client_invoice_create'),
    path('edit/<int:pk>/', views.editupdate_invoice, name='edit_invoice'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('<uuid:special_id>/', views.guest_invoice_detail, name='guest_invoice_detail'),
    path('<uuid:special_id>/pdf/', views.guest_invoice_pdf, name='guest_invoice_pdf'),
    path('newclient/', views.create_new_client, name='create_new_client'),
    path('dashboard', views.dashboard, name='dashboard'),
]