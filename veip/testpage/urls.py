from  django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.newd),
    url(r'^crt', views.pdf),
    url(r'^res', views.res, name='index'),
    # url(r'^test', views.newd),
    url(r'^history', views.history),
    url(r'^rsult',views.resset),
    url(r'^multirsult',views.multires),
    url(r'^change',views.change),
    url(r'^calculations', views.calculations),
    url(r'^theory', views.theory),
    url(r'^viewres', views.viewresult),


]