from django.urls import path
from . import views

app_name='apps.goods'
urlpatterns = [
    path('',views.index,name='index')
]