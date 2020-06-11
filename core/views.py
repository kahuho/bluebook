from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Item


def home(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, "home-page.html", context)
# checkout page view


def checkout(request):
    return render(request, "checkmeout.html")
# products page view


def products(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, "product-page.html", context)
