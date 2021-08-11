from django.contrib import admin


# Register your models here.
from cart.models import CartItem, OrderCart, Address

admin.site.register(CartItem)
admin.site.register(OrderCart)
admin.site.register(Address)