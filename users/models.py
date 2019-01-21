from django.db import models


# Create your models here.


class User(models.Model):
    login_name = models.CharField(max_length=20, unique=True, verbose_name='登录账号')
    name = models.CharField(max_length=20, verbose_name='用户昵称')
    password = models.CharField(max_length=30, verbose_name='用户密码')
    tel = models.CharField(max_length=11, unique=True, null=True, verbose_name='用户电话')
    desc = models.TextField(default=None, null=True, verbose_name='用户简介')
    img = models.ImageField(upload_to='users/', max_length=200, default=None, null=True, verbose_name='用户头像')
