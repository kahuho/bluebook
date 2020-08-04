from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem, BillingAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from django.utils import timezone
from django.contrib import messages


def home(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, "home-page.html", context)
# checkout page view


class CheckoutView(View):
    def get (self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkmeout.html", context)
    def post (self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment = form.cleaned_data.get('apartment')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: Add functionality for billing addr and saving info
                # same_billing_address = form.cleaned_data('same_billing_address')
                # save_biling_info = form.cleaned_data('save_biling_info')
                payment_options = form.cleaned_data.get('street_address')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment=apartment,
                    zip=zip,
                    country=country
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('core:checkout')
            messages.warning(self.request, "Failed to Checkout")
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('core:checkout')



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
