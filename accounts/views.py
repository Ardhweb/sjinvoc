from django.shortcuts import render,redirect

# Create your views here.
from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout                                                 
from django.contrib import auth, messages


# def logout(request):
#     logout(request)
#     return redirect("/")
    
