from django.urls import path
from  . import views

app_name = 'order'

urlpatterns = [
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('coupone/<int:order_id>/', views.coupon_order, name='coupon'),
    # path('request/<int:id><int:price>',send_request,name='request'),
    # path('verify/',verify,name='verify'),
]
