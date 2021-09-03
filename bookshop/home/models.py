from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
# from django.urls import reverse
from django.urls import reverse


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,allow_unicode=True, unique=True, null=True, blank=True)
    # slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category')

    # class Meta:
    #      ordering = ('name',)

    def __str__(self):
        return self.name
    #
    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug, self.id ])


class Writer(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length=150, unique=True ,db_index=True)
	bio = models.TextField()
	pic = models.FileField(upload_to = "writer/")
	createed = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now_add = True)



class Product(models.Model):
    VARIANT = (
        ('None','none'),
        ('Publishe','publish'),
    )
    category = models.ManyToManyField(Category,blank=True) #برقراری بین مدل محصول  و دسته بندی(رابطه یک به چند)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True, null=True, blank=True)
    writer = models.CharField('author', max_length=100, null=True)
    status = models.CharField(null=True, blank=True, max_length=200, choices=VARIANT )
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField(null=True,blank=True)
    information =RichTextUploadingField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product')
    like = models.ManyToManyField(User,blank=True,related_name='product_like')
    total_like= models.IntegerField(default=0)          #تعداد لایکها رو میشماره
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.IntegerField(default=0)


def total_like(self):
        return self.like.count()


def total_unlike(self):
    return self.unlike.count()


    def __str__ (self):
        return self.name

    # برای تغییر رفتار تابع از دکوریتور استفاده میکینم تابع را به یک attribute تبدیل میکنیم
    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return  int(self.unit_price - total)
        return self.total_price

    def get_absolute_url(self):
        return reverse('home:product', args=[self.slug, self.id ])


class Publish(models.Model):
    name = models.CharField(max_length=100)


class Variants(models.Model):
    name = models.CharField(max_length=100)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    publish_variant = models.ForeignKey(Publish,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price