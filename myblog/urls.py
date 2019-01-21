"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from myblog import views

urlpatterns = [
    # 文章
    path('article/', views.article, name='article'),
    path('add_article/', views.add_article, name='add_article'),
    path('update_article/', views.update_article, name='update_article'),
    path('delete_article/', views.delete_article, name='delete_article'),
    # 栏目
    path('category/', views.category, name='category'),
    path('update_category/', views.update_category, name='update_category'),
    path('delete_category/', views.delete_category, name='delete_category'),
    path('delete_session/', views.delete_session, name='delete_session'),
    # 评论
    path('comment/', views.comment, name='comment'),
    # 删除评论
    path('del_comment/', views.del_comment, name='del_comment'),
    # 搜索实现
    path('search_fun/', views.search_fun, name='search_fun'),

]
