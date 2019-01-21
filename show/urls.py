from django.urls import path

from show import views

urlpatterns = [
    path('a_index/', views.a_index, name='a_index'),
    # path('a_services/', views.a_services, name='a_services'),
    path('a_single/', views.a_single, name='a_single'),
    path('a_about/', views.a_about, name='a_about'),
    path('a_tag/', views.a_tag, name='a_tag'),

    # 搜索
    path('search/', views.search, name='search'),
    # 详情,留言
    path('a_contact', views.a_contact, name='a_contact'),
]
