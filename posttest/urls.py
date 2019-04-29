from . import views
from django.conf.urls import  url
from django.urls import path


urlpatterns = [
    url(r'^index/',views.index),
    url(r'^login/',views.login),
    url(r'^login_check/$',views.login_check),
    url(r'^ajax_login/',views.ajax_login),
    url(r'ajax_login_check/',views.ajax_login_check),
]