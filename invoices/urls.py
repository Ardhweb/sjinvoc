from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('guest/create/', views.guest_invoice_create, name='guest_invoice_create'),
    path('client/create/', views.client_invoice_create, name='client_invoice_create'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('dashboard', views.dashboard, name='dashboard'),
]