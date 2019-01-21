from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from myblog.models import Article
from users.forms import RegisterForm, LoginForm
from users.models import User
from django.http import HttpResponseRedirect


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(login_name=username).first()
            request.session['user_id'] = user.id
            # 在这里开始向index页面发送请求,该请求就会被中间件拦截.
            return HttpResponseRedirect(reverse('myblog:article'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            userpwd = form.cleaned_data['userpwd']
            tel = form.cleaned_data['tel']
            User.objects.create(login_name=username, name=name, password=userpwd, tel=tel)
            return HttpResponseRedirect(reverse('users:login'))
        else:
            # 获取表单校验不通过的错误信息
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def update(request):
    if request.method == 'POST':
        truename = request.POST.get('truename')
        usertel = request.POST.get('usertel')
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        user = User.objects.filter(pk=request.user.id).first()
        # 密码修改要使用异步请求
        if not user.password == old_password:
            return render(request, 'article.html', {'msg': ':密码错误'})
        if not password == new_password:
            return render(request, 'article.html', {'msg': ':两次密码不一致'})
        user.name = truename
        user.tel = usertel
        user.password = new_password
        user.save()
        return HttpResponseRedirect(reverse('myblog:article'))


def user_set(request):
    if request.method == 'GET':
        user = request.user
        art_list = Article.objects.filter(user_id=user.id)
        return render(request, 'user_set.html', {'user': user, 'art_list': art_list, 'flag': 4})
    if request.method == 'POST':
        user = request.user
        user.img = request.FILES.get('user_img')
        user.desc = request.POST.get('desc')
        user.save()
        return HttpResponseRedirect(reverse('users:user_set'))
