from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name = 'register'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('profile/', views.user_profile,name='profile'),
    path('update/', views.user_update,name='update'),
    path('change/', views.change_password,name='change'),
    path('active/<uidb64>/<token>/', views.RegisterEmail.as_view(),name='active'),
    path('reset/', views.ResetPassword.as_view(),name='reset'),
    path('reset/done/', views.DonePassword.as_view(),name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(),name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(),name='complete'),
    # path('login_phone/', views.phone,name='phone'),
    # path('verify/', views.verify,name='verify'),
]