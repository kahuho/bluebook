from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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


class OrderSummary(LoginRequiredMixin, View):
    def get(self, * args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order

            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

@login_required
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
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item succcesfully added to your cart")
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:order_summary")


# removing items from the cart

@login_required
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
            return redirect("core:order_summary")


        else:
            # add message order doesnt exist
            messages.info(request, "Item does not exists in your cart")
            return redirect("core:order_summary")
    else:
        messages.info(request, "You do not have an active order yet")
        return redirect("core:product")

# romove single item from order summary
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    # confirm whether item alreday exists in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.warning(request, "Item quantity was updated")
            return redirect("core:order_summary")


        else:
            # add message order doesnt exist
            messages.info(request, "Item does not exists in your cart")
            return redirect("core:order_summary")
    else:
        messages.info(request, "You do not have an active order yet")
        return redirect("core:product")
