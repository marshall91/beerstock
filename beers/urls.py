from django.conf.urls import patterns, url

from beers import views

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'beers/login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/beers/successfully_logged_out/'}),
	url(r'^successfully_logged_out/$', views.logged_out, name='logout'),
	
	url(r'^search_beer/$', views.search_beer, name='search_beer'),
	url(r'^update_beer/(?P<bid>[0-9]+)/$', views.update_beer, name='update_beer'),
	url(r'^checkout_beer/(?P<bid>[0-9]+)/$', views.checkout_beer, name='checkout_beer'),
	url(r'^stock_index/$', views.stock_index, name='stock_index'),
	url(r'^history_index/$', views.history_index, name='history_index'),
	url(r'^account_info/$', views.account_info, name='account_info'),
	url(r'^account_auth/$', views.account_update, name='account_update'),
)