from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# from home.models import *
from django.forms import ModelForm
from order.models import Order
# from bookshop.home.models import *
# from bookshop.home.models import Product
from home.models import Variants, Product


class Cart(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.CASCADE )
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
