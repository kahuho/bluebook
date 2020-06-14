from django.urls import path
from .views import home, checkout, ItemView, HomeView, products, add_to_cart
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('products/', products, name='products'),
    path('product/<slug>/', ItemView.as_view(), name='product'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart')

]
