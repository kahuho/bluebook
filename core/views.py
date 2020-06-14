from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem


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


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"
    # detailed view of single item


class ItemView(DetailView):
    model = Item
    template_name = "product-page.html"

# adding items to cart


def add_to_cart(requets, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order_item = order_qs[0]
        # confirm whether item alreday exists in order
        if order.items.filter(item__slug=item.slug). exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order = Order.objects.create(user=requet.user)
            order.items.add(order_item)
        return redirect("core:product", slug=slug)
