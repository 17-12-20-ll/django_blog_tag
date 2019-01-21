from django.db import models

# Create your models here.


from users.models import User


# 栏目
class Columns(models.Model):
    name = models.CharField(max_length=10, unique=True, null=False, verbose_name='栏目名称')
    alias = models.CharField(max_length=20, null=True, verbose_name='栏目别名')
    keyword = models.CharField(max_length=50, null=True, verbose_name='栏目关键字')
    desc = models.CharField(max_length=200, null=True, verbose_name='栏目描述')
    columns = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, related_name='coll',
                                verbose_name='栏目父节点')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')


# 文章
class Article(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    keyword = models.CharField(max_length=30, verbose_name='关键字')
    describe = models.CharField(max_length=100, verbose_name='文章描述')
    title_img = models.ImageField(upload_to='article/', max_length=200, verbose_name='文章封面')
    state = models.CharField(choices=(('publish', '公布'), ('private', '私密')), max_length=10, verbose_name='发布状态')
    col = models.ForeignKey(Columns, related_name='col', on_delete=models.SET_NULL, null=True, verbose_name='所属栏目')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True, verbose_name='所属作者')
    # 软删除-------增加is_delete字段
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


# 标签
class Label(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='标签名称')
    article = models.ManyToManyField(Article, related_name='lab', verbose_name='多对多文章')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')


# 评论
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='com', on_delete=models.CASCADE, verbose_name='所属人')
    content = models.CharField(max_length=200, verbose_name='评论内容')
    article = models.ForeignKey(Article, related_name='com', on_delete=models.CASCADE, verbose_name='评论的文章')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')


# 留言
class Ly(models.Model):
    toUser = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='tou', verbose_name='接收留言人')
    content = models.CharField(max_length=200, verbose_name='留言内容', default=None, null=True)
    fromUser = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='fromu', verbose_name='留言人')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
