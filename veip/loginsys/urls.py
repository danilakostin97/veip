
from django.urls import include
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^$', views.checkauth, name='logout'),
]