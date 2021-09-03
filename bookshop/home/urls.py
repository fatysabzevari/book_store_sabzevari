from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.home, name = 'home'),
    path('product/',views.all_product, name = 'product'),
    path('detail/<int:id>/',views.product_detail, name = 'detail'),
    path('category/<slug>/<int:id>/',views.all_product, name = 'category'), #برای اینکه کاراکترهای فارسی را بخواند و ارور ندهد نوعش رو مشخص نمیکنیم
    path('writer/<int:id>/', views.get_writer, name = 'writer'),
    path('like/<int:id>/', views.product_like, name = 'product_like'),
    path('unlike/<int:id>/', views.product_unlike, name = 'product_unlike'),
    path('search/',views.product_search, name = 'product_search'),
]