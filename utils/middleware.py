import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from users.models import User


class IsLoginMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        try:
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            request.user = user
            return None
        except Exception as e:
            path = request.path
            if path == '/':
                return None
            # if re.match('/show/.*', path):
            #     return HttpResponseRedirect(reverse('users:a_login'))
            if path == '/show/a_contact':
                return HttpResponseRedirect(reverse('users:login'))
            for i in ['/users/login/', '/users/register/', '/show/.*',
                      '/media/article/.*']:
                if re.match(i, path):
                    # 跳过以下代码,直接访问对应的视图
                    return None
            return HttpResponseRedirect(reverse('users:login'))
