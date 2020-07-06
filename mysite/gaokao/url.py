from django.urls import path

from . import views

app_name = 'gaokao'
urlpatterns = [
    # ex: /polls/
    path('listmeta', views.listmeta, name='listmeta'),
    path('list', views.list, name='list'),
    path('detail', views.detail, name='detail'),
    # ex: /polls/5/
    # path('<str:school_id>/', views.detail, name='detail'),
]
