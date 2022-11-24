from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register((Maincategory,Subcategory,Brand,Product,Buyer,Wishlist,Checkout,CheckoutProducts,Contact))
