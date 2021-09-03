from django.contrib import admin
from .models import Cart, CartForm

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','variant', 'quantity',]
    # list_filter = ['product']

admin.site.register(Cart)
# admin.site.register(CartForm)