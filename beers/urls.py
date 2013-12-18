from django.conf.urls import patterns, url

from beers import views

urlpatterns = patterns('',
	url(r'^stock_index/$', views.stock_index, name='stock_index'),
	url(r'^beer_index/$', views.beer_index, name='beer_index'),
	url(r'^brewery_index/$', views.brewery_index, name='brewery_index'),
	url(r'^beer_type_index/$', views.beer_type_index, name='beer_type_index'),
	url(r'^add_new_beer/$', views.add_new_beer, name='add_new_beer'),
	url(r'^add_new_brewery/$', views.add_new_brewery, name='add_new_brewery'),
	url(r'^add_new_type/$', views.add_new_type, name='add_new_type'),
	url(r'^beer_info/(?P<beer_name>[a-zA-Z0-9" "]+)/$', views.beer_detail, name='beer_detail'),
	url(r'^brewery_info/(?P<brewery_name>[a-zA-Z0-9" "]+)/$', views.brewery_detail, name='brewery_detail'),
	url(r'^beer_type_info/(?P<beer_type_name>[a-zA-Z0-9" "]+)/$', views.beer_type_detail, name='beer_type_detail'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'beers/login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/beers/successfully_logged_out/'}),
	url(r'^successfully_logged_out/$', views.logged_out, name='logout'),
)