from django.contrib.auth.models import User
from django.db import models
# from account.models import BaseUser, Address
# from home.models import *
from django.forms import ModelForm

from home.models import Product, Variants


class Order(models.Model):
    # STATUS = [('done', 'Done'), ('in_process', 'In_process'), ('in_basket', 'In_basket')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # date = models.DateTimeField(auto_now_add=True)
    create = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    email= models.EmailField()
    f_name = models.CharField(max_length=100, null=True, blank=True)
    l_name = models.CharField(max_length=100, null=True, blank=True)
    # total_price = models.PositiveIntegerField(default=0)
    # status = models.CharField(max_length=10, choices=STATUS, default='In_basket')
    # address = models.CharField( on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    # code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class ItemOrder(models.Model):
    order =models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username.publish_variant.name

    def publish(self):
        return self.variant


    def price(self):
        if self.product.status !='None':
            return self.variant.total_price * self.quantity
        else:
            return self.variant.total_price * self.quantity
# class ShoppingCart(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, related_name='order_item')
#     order = models.ForeignKey(Ordering, on_delete=models.DO_NOTHING, null=True, related_name='order')
#     user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
#     number = models.IntegerField(null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#     def price(self):
#         return self.book.total_price * self.book.Inventory
#
#
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email','address', 'f_name', 'l_name']

#
class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)#از قبل مقدار دهی شده
    active = models.BooleanField(default=False)  #کد تخفیف فعال هست یا نه
    start = models.DateTimeField() #تاریخ شروع کد
    end = models.DateTimeField()  #انقضای کد
    discount = models.PositiveIntegerField()  #میزان درصد تخفیف
