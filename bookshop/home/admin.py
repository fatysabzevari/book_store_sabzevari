from django.contrib import admin
from .models import *

class ProductVariantInlines(admin.TabularInline):
    model = Variants


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','created','updated','sub_category')
    list_filter = ('created',)
    prepopulated_fields = {
        'slug':('name',)
    }

class AddWriter(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {
        'slug': ('name',)
    }

admin.site.register(Writer, AddWriter)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated', 'amount','available','unit_price', 'discount', 'total_price',]
    list_filter = ('available',)
    list_editable = ('amount',)
    raw_id_fields = ('category',)
    inlines = [ProductVariantInlines]
                                 #slug را خود جنگو وارد میکند
# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variants)
admin.site.register(Publish)