from django.db import models

from accounts.models import BaseUser
from catalog.models import Books

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    books = models.ForeignKey('catalog.Books', unique=False, on_delete=models.CASCADE,)
#سبد
    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def total(self):
        return self.quantity * self.books.price

    def name(self):
        return self.books.name

    def price(self):
        return self.books.price

    # def get_absolute_url(self):
    #     return self.books.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()


class OrderCart(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)


class Address(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderCart, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=200, null=False)
    post_id = models.IntegerField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)