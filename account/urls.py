from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/account/successfully_logged_out/'}),
    url(r'^successfully_logged_out/$', views.logged_out, name='logout'),
    url(r'^account_settings/$', views.account_settings, name='account_settings'),
    url(r'^account_auth/$', views.account_update, name='account_update'),
    url(r'^signup/$', views.signup, name='signup'),
)
