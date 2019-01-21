import re

from django import forms

from users.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=3, required=True,
                               error_messages={
                                   'required': '登录名必填',
                                   'max_length': '登录名不能超过10字符',
                                   'min_length': '登录名不能少于3字符'
                               })
    name = forms.CharField(max_length=10, min_length=2, required=True,
                           error_messages={
                               'required': '用户昵称必填',
                               'max_length': '用户昵称不能超过10字符',
                               'min_length': '用户昵称不能少于2字符'
                           })

    userpwd = forms.CharField(max_length=10, min_length=3, required=True,
                              error_messages={
                                  'required': '密码必填',
                                  'max_length': '密码不能超过10字符',
                                  'min_length': '密码不能少于3字符'
                              })

    reuserpwd = forms.CharField(max_length=10, min_length=3, required=True,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码不能超过10字符',
                                    'min_length': '密码不能少于3字符'
                                })

    tel = forms.CharField(required=True, error_messages={
        'required': '电话必填',
    })

    def clean_username(self):
        # 校验注册的账号已存在
        username = self.cleaned_data['username']
        user = User.objects.filter(login_name=username).first()
        if user:
            raise forms.ValidationError('抱歉,该账号已存在,请更换账号注册!')
        return self.cleaned_data['username']

    def clean(self):
        # 校验密码是否一致
        userpwd = self.cleaned_data.get('userpwd')
        reuserpwd = self.cleaned_data.get('reuserpwd')
        if userpwd != reuserpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data

    def clean_tel(self):
        # 校验电话是否符合要求
        tel = self.cleaned_data.get('tel')
        tel_regx = '(13\d|14[579]|15[4]|17[49]|18\d)\d{8}'
        if not re.match(tel_regx, tel):
            raise forms.ValidationError('电话格式错误')
        return self.cleaned_data['tel']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=3, required=True,
                               error_messages={
                                   'required': '登录名必填',
                                   'max_length': '登录名不能超过10字符',
                                   'min_length': '登录名不能少于3字符'
                               })
    userpwd = forms.CharField(max_length=10, min_length=3, required=True,
                              error_messages={
                                  'required': '密码必填',
                                  'max_length': '密码不能超过10字符',
                                  'min_length': '密码不能少于3字符'
                              })

    def clean(self):
        # 用户名是否已经注册
        username = self.cleaned_data.get('username')
        user = User.objects.filter(login_name=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册,请先注册'})
        # 校验密码
        userpwd = self.cleaned_data.get('userpwd')
        if userpwd != user.password:
            raise forms.ValidationError({'userpwd': '用户密码错误'})
        return self.cleaned_data
