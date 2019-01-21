from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from myblog.models import Article, Label, Comment
from users.models import User


def a_index(request):
    if request.method == 'GET':
        art_list = Article.objects.all()
        return render(request, 'a_index.html', {'art_list': art_list, 'flag': 1})


def a_about(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            return render(request, 'a_about.html', {'user': user, 'flag': 2})
        return render(request, 'a_about.html', {'no_user': '当前没有登录用户', 'flag': 2})


def a_single(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        art = Article.objects.get(pk=id)
        # 加上限制条件,进行发布最新,最热文章,根据点击榜推荐
        new_art_list = Article.objects.all().order_by('-add_time')[:4]
        comment_list = Comment.objects.filter(article_id=id).all()
        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(id)
        art_id_max = Article.objects.all().order_by('-id').first()
        id_max = art_id_max.id  # 文章最大id
        while not has_prev and id_prev >= 1:
            art_prev = Article.objects.filter(id=id_prev - 1).first()
            if not art_prev:
                # 没有这个id的文章
                id_prev -= 1
            else:
                # 有前一篇
                has_prev = True
        while not has_next and id_next <= id_max:
            art_next = Article.objects.filter(id=id_next + 1).first()
            if not art_next:
                # 没有这个id的文章
                id_next += 1
            else:
                # 有后一篇
                has_next = True
        return render(request, 'a_single.html',
                      {'art': art, 'new_art_list': new_art_list, 'comment_list': comment_list, 'has_prev': has_prev,
                       'has_next': has_next, 'art_prev': art_prev, 'art_next': art_next})
    if request.method == 'POST':
        id = request.session.get('user_id')
        if id:
            comment = request.POST.get('comment')
            user = request.user
            article_id = int(request.GET.get('id'))
            Comment.objects.create(content=comment, article_id=article_id, user_id=user.id)
            return HttpResponseRedirect(f'/show/a_single/?id={article_id}')
        else:
            return HttpResponseRedirect(reverse('users:login'))


def a_contact(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        user = User.objects.get(pk=id)
        return render(request, 'a_about.html', {'user': user, 'flag': 2})


# def a_services(request):
#     if request.method == 'GET':
#         return render(request, 'a_login.html')


def a_tag(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if not id:
            # 删除没有文章对应的标签
            lab_list = Label.objects.all()
            for l in lab_list:
                if not l.article.filter():
                    Label.objects.filter(pk=l.id).delete()
            lab_list = Label.objects.all()
            return render(request, 'a_tag.html', {'lab_list': lab_list, 'flag': 3})
        else:
            lab = Label.objects.filter(pk=id).first()
            l_list = lab.article.all()
            return render(request, 'a_list.html', {'l_list': l_list, 'flag': 3})


def search(request):
    if request.method == "GET":
        art_name = request.GET.get('name')
        art_list = Article.objects.filter(Q(title__contains=art_name) | Q(keyword__contains=art_name)).all()
        return render(request, 'a_list.html', {'l_list': art_list, 'flag': 1})
