from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


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
    paginate_by = 8
    template_name = "home-page.html"
    # detailed view of single item


class ItemView(DetailView):
    model = Item
    template_name = "product-page.html"

# adding items to cart


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # confirm whether item alreday exists in order
        if order.items.filter(item__slug=item.slug). exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quanity was updated")

        else:
            order.items.add(order_item)
            messages.info(request, "Item succcesfully added to your cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product", slug=slug)


# removing items from the cart


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    # confirm whether item alreday exists in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.warning(request, "Item removed from your cart")

        else:
            # add message order doesnt exist
            messages.info(request, "Item does not exists in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order yet")
        return redirect("core:product")
    return redirect("core:product", slug=slug)
