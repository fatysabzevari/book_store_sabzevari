from datetime import timezone

from django.db import models
from django.urls import reverse
class Category(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50, unique=True,
        help_text='Unique value for books page URL, created from name.')
  description = models.TextField()
  is_active = models.BooleanField(default=True)
  meta_keywords = models.TextField('meta_keywords', max_length=255,
        help_text='Comma-delimited set of SEO keywords for meta tag')
  meta_description = models.CharField("Meta Description", max_length=255,
        help_text='Content for description meta tag')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
   db_table = 'categories'
   ordering = ['-created_at']
   verbose_name_plural = 'Categories'

  def __str__(self):
   return self.name

  # @models.permalink
  class MyModel(models.Model):

    def get_absolute_url(self):
        return ('catalog_category', (), { 'category_slug': self.slug })


class Books(models.Model):
     name = models.CharField(max_length=255, unique=True)
     slug = models.SlugField(max_length=255, unique=True,
          help_text='Unique value for books page URL, created from name.')
     # brand = models.CharField(max_length=50)
     sku = models.CharField(max_length=50)
     # author = models.CharField('author', max_length=100, null=True)
     # published_year = models.DateTimeField('published year', blank=True, null=True, default=timezone.now)
     price = models.DecimalField(max_digits=9,decimal_places=2)
     old_price = models.DecimalField(max_digits=9,decimal_places=2,
          blank=True,default=0.00)
     image = models.ImageField(upload_to='images/', null=True, blank=True)
     is_active = models.BooleanField(default=True)
     is_bestseller = models.BooleanField(default=False)
     is_featured = models.BooleanField(default=False)
     quantity = models.IntegerField()
     description = models.TextField()
     meta_keywords = models.CharField(max_length=255,
          help_text='Comma-delimited set of SEO keywords for meta tag')
     meta_description = models.CharField(max_length=255,
          help_text='Content for description meta tag')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     categories = models.ManyToManyField(Category)

     class Meta:
           db_table = 'books'
           ordering = ['-created_at']


     def __str__(self):
        return self.name

     # @models.permalink
     class MyModel(models.Model):
        def get_absolute_url(self):
            return ('catalog_books', (), {'books_slug': self.slug})

     def sale_price(self):
        if self.old_price > self.price:
            return self.price

        else:
            return None
