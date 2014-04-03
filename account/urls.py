from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    url(r'^account_info/$', views.account_info, name='account_info'),
    url(r'^account_auth/$', views.account_update, name='account_update'),
    url(r'^signup/$', views.signup, name='signup'),
)
