from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


# 注册页面表单（推荐用这个）
class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone_number")


# 主页页面表单（这是自己写的form)
class UserRegisterForm2(forms.Form):
    email = forms.EmailField(label='邮箱')
    username = forms.CharField(label='用户名', max_length=64)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='再次确认密码', widget=forms.PasswordInput())


class UserLoginForm(forms.Form):
    email = forms.CharField(label='邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
