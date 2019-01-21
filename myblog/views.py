from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from myblog.models import Columns, Label, Article, Comment
from django.http import HttpResponseRedirect, JsonResponse


def article(request):
    if request.method == 'GET':
        user_id = request.user.id
        # 分页
        # 获取分页的脚码
        page = int(request.GET.get('page', 1))
        # 使用Paginator库实现分页
        art_list = Article.objects.all().filter(user_id=user_id).order_by('-add_time')  # 按照最新排序
        paginator = Paginator(art_list, 5)  # 参数:第一个参数-所有该表过滤后的对象,第二个参数-分页条数
        art_list = paginator.page(page)
        return render(request, 'article.html', {'art_list': art_list, 'flag': 1})


def add_article(request):
    if request.method == 'GET':
        col_list = Columns.objects.all()
        c_id = request.GET.get('c_id')
        if c_id:
            return render(request, 'add-article.html', {'col_list': col_list, 'c_id': c_id, 'flag': 1})
        else:
            return render(request, 'add-article.html', {'col_list': col_list, 'flag': 1})
    if request.method == 'POST':
        title = request.POST.get('title')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        category_id = int(request.POST.get('category'))
        content = request.POST.get('content')
        state = request.POST.get('visibility')
        cover = request.FILES.get('titlepic')
        # user_id  登录后将数据存入session,使用中间件
        user_id = request.user.id
        art = Article()
        art.title = title
        art.keyword = keywords
        art.describe = describe
        art.col_id = category_id
        art.content = content
        art.state = state
        art.title_img = cover
        art.user_id = user_id
        art.save()
        for t in request.POST.get('tags').split(','):
            if Label.objects.filter(name=t).first():
                art.lab.add(Label.objects.filter(name=t).first())  # 给文章添加标签
            else:
                Label.objects.create(name=t)
                art.lab.add(Label.objects.filter(name=t).first())  # 给文章添加标签
        return HttpResponseRedirect(reverse('myblog:article'))


def update_article(request):
    art = Article.objects.get(id=request.GET.get('id'))
    if request.method == 'GET':
        col_list = Columns.objects.all()
        return render(request, 'update-article.html', {'art': art, 'col_list': col_list, 'flag': 1})
    if request.method == 'POST':
        title = request.POST.get('title')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        category_id = int(request.POST.get('category'))
        content = request.POST.get('content')
        state = request.POST.get('visibility')
        cover = request.FILES.get('titlepic')
        # user_id  登录后将数据存入session,使用中间件
        user_id = request.user.id
        art.title = title
        art.keyword = keywords
        art.describe = describe
        art.col_id = category_id
        art.content = content
        art.state = state
        art.title_img = cover
        art.user_id = user_id
        art.lab.clear()
        art.save()
        for t in request.POST.get('tags').split(','):
            if Label.objects.filter(name=t).first():
                art.lab.add(Label.objects.filter(name=t).first())  # 给文章添加标签
            else:
                Label.objects.create(name=t)
                art.lab.add(Label.objects.filter(name=t).first())  # 给文章添加标签
        return HttpResponseRedirect(reverse('myblog:article'))


@csrf_exempt
def delete_article(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        Article.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('myblog:article'))


def category(request):
    if request.method == 'GET':
        col_list = Columns.objects.all()
        back_list = []
        group_list = []
        for col_root in col_list:
            curLevel = [col_root]  # 将父栏目放在列表中,方便下一级父栏目添加在列表中
            temp = []  # 遍历当前层级时存放的临时节点值
            while curLevel:
                nextLevel = []  # 下一层树结点
                for j in curLevel:  #
                    for col_val in j.col.all():
                        temp.append(col_val)
                    if j.coll.all():  # 当前结点是否存在子结点
                        for level_val in j.coll.all():
                            nextLevel.append(level_val)
                curLevel = nextLevel
            back_list.append([len(temp), temp])
        for ii in range(len(back_list)):
            group_list.append([col_list[ii], back_list[ii]])
        if not request.GET.get('col_id'):
            return render(request, 'category.html', {'group_list': group_list, 'flag': 3})
        else:
            # group_list 结构为:[[栏目,[该栏目数量,栏目下的所有文章]],[栏目,[该栏目数量,栏目下的所有文章]]]
            id = request.GET.get('col_id')
            for g in group_list:
                if g[0].id == int(id):
                    art_list = g  # [栏目,[该栏目数量,栏目下的所有文章]]
                    break
            return render(request, 'art_list_cate.html', {'art_list': art_list, 'flag': 3})

    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        columns_id = request.POST.get('fid')
        keyword = request.POST.get('keywords')
        desc = request.POST.get('describe')
        Columns.objects.create(name=name, alias=alias, columns_id=columns_id, desc=desc, keyword=keyword)
        return HttpResponseRedirect(reverse('myblog:category'))


def update_category(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        category_id = Columns.objects.get(pk=id)
        category_list = Columns.objects.all()
        return render(request, 'update-category.html',
                      {'category_id': category_id, 'category_list': category_list, 'flag': 3})
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        fid = request.POST.get('fid')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        if all([name, alias, keywords, describe]):
            col = Columns.objects.get(name=name)
            col.name = name
            col.alias = alias
            col.columns_id = fid
            col.keyword = keywords
            col.desc = describe
            col.save()
            return HttpResponseRedirect(reverse('myblog:category'))
        else:
            return render(request, 'update-category.html', {'flag': 3})


@csrf_exempt
def delete_category(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        Columns.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('myblog:category'))


# 退出删除session
@csrf_exempt
def delete_session(request):
    if request.method == 'POST':
        request.session.flush()
        return HttpResponseRedirect(reverse('myblog:article'))


# 评论
def comment(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        art_list = Article.objects.filter(user_id=request.user.id)
        com_list = Comment.objects.filter(article_id__in=art_list).order_by('-add_time')
        # 组装数据[评论人,评论文章,内容,日期]
        result = []
        for c in com_list:
            # c.user.name  # 评论人
            # c.article.title  # 评论文章
            # c.content  # 评论内容
            # c.add_time  # 评论时间
            data = [c.user.name, c.article.title, c.content, c.add_time, c.id]
            result.append(data)
            # 结构 [[],[],...]
        pg = Paginator(result, 5)
        result = pg.page(page)
        return render(request, 'comment.html', {'result': result, 'flag': 2})


@csrf_exempt
def del_comment(request):
    if request.method == "POST":
        com_id = request.POST.get('com_id')
        Comment.objects.filter(id=com_id).delete()
        return JsonResponse({'code': 200, 'msg': 'success'})


def search_fun(request):
    if request.method == 'GET':
        user_id = request.user.id
        page = int(request.GET.get('page', 1))
        text = request.GET.get('text')
        art_list = Article.objects.filter(
            Q(title__contains=text) | Q(keyword__contains=text) | Q(describe__contains=text)).filter(user_id=user_id)
        paginator = Paginator(art_list, 5)  # 参数:第一个参数-所有该表过滤后的对象,第二个参数-分页条数
        art_list = paginator.page(page)
        return render(request, 'article.html', {'art_list': art_list, 'flag': 1})
