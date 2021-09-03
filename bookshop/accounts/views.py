import ghasedak
from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from home.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# from random import randint
# Create your views here.

class EmailToken(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))
email_generator = EmailToken()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'], email= data['email'], first_name=data['first_name'], last_name=data['last_name'], password=data['password_2'])
            user.is_active = False   #به صورت پیش فرض هر کسی ثبت نام کند فعال نیست
            # messages.success(request, 'خوش آمدید','primary')
            user.save()
            domain = get_current_site(request).domain

            uidb64 =  urlsafe_base64_encode(force_bytes(user.id))       #userid base 64
            url = reverse('accounts:active', kwargs={'uidb64': uidb64,'token':email_generator.make_token(user)})
            link = 'http://' + domain + url

            email = EmailMessage(
                'active user',
                # 'hi user',
                 link,
                'test<sabzevarifatemeh0188@gmail.com>',
                [data['email']],

            )
            email.send(fail_silently=False)  #دیدن خطای ایمیل
            messages.warning(request,'لطفا برای فعالسازی به ایمیل خود مراجعه کنید','warning')
            return redirect('home:home')

            # clean
    else:
        form = UserRegisterForm()

    return render(request,'accounts/register.html', {'form': form})

class RegisterEmail(View):     #classs base view

    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))       #کد را خوانا میکند
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username= User.objects.get(email=data['user']), password=data['password']) #check user&password
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'خوش آمدید','primary')
                return redirect('home:home')
            else:
                messages.error(request,'user or password wrong','danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form':form})

def user_logout(request):
    logout(request)
    messages.success(request,'با موفقیت خارج شدید', 'warning')
    return redirect('home:home')




@login_required(login_url='accounts:login')
#اول به صفحه لاگین برود
def user_profile(request):
    profile = Profile.objects.get(user_id= request.user.id)    #چون لاگین بودیم و به ای دی یوزر دسترسی داشتیم در اینجا بر اساس ای دی یوزر پروفایل را مشخص کردیم
    return render(request, 'accounts/profile.html', {'profile' : profile})

@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)    #بین مدل یوزر و پروفایل رابطه وان تو وان ایجاد کردیم
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'update successfully', 'success')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = { 'user_form':user_form, 'profile_form':profile_form}
    return render(request,'accounts/update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, 'پسورد با موفقیت تغییر کرد', 'success')
            return redirect('accounts:profile')
        else:
            messages.error(request,'پسورد اشتباه است','danger')
            return redirect('accounts:change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change.html', {'form' : form})

# def phone(request):
#     if request.method == 'POST':
#         form = PhoneForm(request.POST)
#         if form.is_valid():
#             global random_code         #دسترسی به کد در قسمتverify
#             data = form.cleaned_data
#             phone = f"{data['phone']}"    #اگر بخواهیم شماره همراه وارد کنیم چون از اینتیجر فیلد استفاده کردبم صفر اول را نمیندازه و بهتره از f''استفاده کنیم
#             random_code = randint(100,1000)   #عدد ارسالی بین 100 و 100 باشد
#             sms = ghasedak.Ghasedak("6a204de856b9b88b1fdd325d8ddfdea0619ee011a95c981ff8d3f82a46fd1353")
#             sms.send({ 'message' : random_code,'receptor' : phone ,'linenumber':"10008566"})
#             return redirect('accounts:verify')
#     else:
#         form = PhoneForm()
#     return render(request, 'accounts/phone.html', {'form':form})
#
# def verify(request):
#     if request.method == 'POST':
#         form = CodeForm(request.POST)
#         if form.is_valid():
#             if random_code == form.cleaned_data['code']:
#                 profile= Profile.objects.get(phone=phone)  #بر اساس شماره همراه کاربر را لاگین میکنیم
#                 user = User.objects.get(profile__id = profile.id)         #استفاده از field look up# با استفاده از آی دی پروفایل مشخص میشه متعلق به کدوم یوزر هست
#                 login(request,user)
#                  messages.success(request, 'سلام ')
#                  return redirect('home:home')
#                 else:
#                     messages.error(request, 'کد اشتباه است')

#
#
#
#
#     else:
#         form= CodeForm()
#
#
#     return render(request, 'accounts/code.html', {'form': form})


class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done') #کاربر را به صفحه خاصی هدایت میکنیم
    email_template_name = 'accounts/link.html'

class DonePassword(auth_views.PasswordResetView):
    template_name = 'accounts/done.html'  #یک فایل html مشخص میکینم

class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:complete')

class Complete (auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'