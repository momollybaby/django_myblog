from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail

from .forms import UserRegisterForm, UserLoginForm
from .models import User
from .token import Token
from my_blog.my_blog.settings import SECRET_KEY

token_confirm = Token(SECRET_KEY)


# Create your views here.

# 注册页面（推荐用这个）
def register(request):
    # 从get或者post请求中获取next参数值
    # get请求中，next通过url传递，即/?next=value
    # post请求中，next通过表单传递，即<input type ="hidden" name="next" value="{{ next }}" />
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # "清洁"表单————把它们转换为其他正确的格式
            cd = form.cleaned_data
            username, email, phone_number, password = cd['username'], cd['email'], cd['phone_number'], cd['password1']
            user = User.objects.create_user(username=username, email=email, phone_number=phone_number,
                                            password=password, is_active=False)
            user.set_password(password)
            user.save()
            token = token_confirm.generate_validate_token(username)
            # active_key = base64.encodestring(username)
            # send email to the register email
            message = "\n".join([u'{0}, 欢迎加入我的博客'.format(username),
                                 u'请访问该链接，完成用户验证：',
                                 '/'.join(['account/active', token])])
            send_mail(u'注册用户验证信息', message, None, [cd['email']])
            # user = auth.authenticate(username=username, password=password)
            # auth.login(request, user)
            return HttpResponse(u'请登录注册邮箱以完成用户验证，有效期为一个小时。')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', context={'form': form})


# 处理注册邮件验证
def active_user(request, token):
    """the view function is used to accomplish the user register confirm, only after input the link that sent to
       the register email,user can login the site normally.
       :param request:
       :param activate_key:the paragram is gotten by encrypting username when user register
       :return:"""
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已经过期')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(u'对不起，您所验证的用户不存在，请重新注册')
    user.is_active = True
    user.save()
    return HttpResponseRedirect(request, 'registration/login.html', context={'message': '验证成功，请登陆'})


# 注册页面（这是自己写的代码）并没有调用此视图
def register2(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            email_results = User.objects.filter(email=email)
            if len(email_results) > 0:
                return render(request, 'blog/register.html', context={'error_message': '邮箱已存在'})
            username = form.cleaned_data['username']
            username_results = User.objects.filter(username=username)
            if len(username_results) > 0:
                return render(request, 'blog/register.html', context={'error_message': '用户名已存在'})
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password != password2:
                return render(request, 'blog/register.html', context={'error_message': '两次输入密码不一致'})
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            return HttpResponseRedirect(reverse('blog:register_success'))
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', context={'form': form})


def success(request):
    return render(request, 'blog/register_success.html')


# 自己写的登录视图，但并没有调用
def blog_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:login_success'))
            else:
                return render(request, 'blog/login.html', context={'error_message': '用户账号或密码错误'})
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', context={'form': form})


def index(request):
    return render(request, 'index.html')
