from django.urls import path
from . import views

urlpatterns = [
    path('item/', views.item_list, name='列表展示'),
    path('info/service/<str:name>', views.info_service, name='服务查询'),
    path('info/access/<str:name>', views.info_access, name='接入查询')
]