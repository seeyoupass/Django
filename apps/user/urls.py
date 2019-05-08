from django.urls import path
from django.conf.urls import url
from . import views
from .views import RegisterView,ActiveView,LoginView

app_name='apps.user'
urlpatterns =[
    #url(r'^register$',views.register,name='register'),
    #url(r'^register_handle$',views.register_handle,name='register_handle'),
    url(r'^register$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),
    url(r'^login$',LoginView.as_view(),name='login')
]