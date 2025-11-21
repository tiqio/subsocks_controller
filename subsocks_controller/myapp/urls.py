from django.urls import path
from . import views

urlpatterns = [
    path('item/', views.item_list, name='列表展示')
]