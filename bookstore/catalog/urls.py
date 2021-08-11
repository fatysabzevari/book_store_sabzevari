from django.urls import path
from .views import *


urlpatterns = patterns('bookstore.catalog.views',
 (r'^$', 'index', { 'template_name':'catalog/index.html'}, 'catalog_home'),
 (r'^category/(?P<category_slug>[-\w]+)/$',
 'show_category', {
'template_name':'catalog/category.html'},'catalog_category'),
 (r'^books/(?P<books_slug>[-\w]+)/$',
 'show_books', {
'template_name':'catalog/books.html'},'catalog_books'),
)

urlpatterns =[
    path('',views.index, name='index')
]