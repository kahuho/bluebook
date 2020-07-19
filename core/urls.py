from django.urls import path
from .views import home, checkout, ItemView, HomeView, products, add_to_cart, remove_from_cart, OrderSummary, remove_single_item_from_cart
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('products/', products, name='products'),
    path('product/<slug>/', ItemView.as_view(), name='product'),
    path('order_summary', OrderSummary.as_view(), name='order_summary'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart')

]
