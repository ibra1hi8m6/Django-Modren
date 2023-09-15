from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([
    Category,
    Subcategory,
    Product,
    ProductImage,
    ProductInfoSection,
    Review,
    Coupon,
    Cart,
    CartItem,
    Checkout
])