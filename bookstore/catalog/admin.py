from django.contrib import admin
from .models import Books, Category
# from bookstore.catalog.forms import BooksAdminForm

# Register your models here.
class BooksAdmin(admin.ModelAdmin):
     # form = BooksAdminForm
     # sets values for how the admin site lists your books
     list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at',)
     list_display_links = ('name',)
     list_per_page = 50
     ordering = ['-created_at']
     search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
     exclude = ('created_at', 'updated_at',)

     # sets up slug to be generated from books name
     prepopulated_fields = {'slug': ('name',)}

# registers your books model with the admin site
admin.site.register(Books, BooksAdmin)


class CategoryAdmin(admin.ModelAdmin):
    # sets up values for how admin site lists categories
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)

    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
