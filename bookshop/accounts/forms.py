from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(forms.Form):

    user_name = forms.CharField(max_length=50)
    email= forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password_1 = forms.CharField(max_length=50)
    password_2 = forms.CharField(max_length=50)

    def clean_user_name(self):
    #اعتبار سنجی#
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('user exist')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل از قبل وجود دارد')
        return email

    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('اpassword not match')
        elif len(password2) < 8:
            raise forms.ValidationError('password too short ')
        elif not any (x.isupper() for x in password2):
            raise forms.ValidationError('باید حداقل یک حروف بزرگ داشته باشد')
        return password1

class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address']