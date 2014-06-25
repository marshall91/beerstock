from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^beers/get/stock', views.get_stock, name='get_stock'),
    url(r'^beers/get/beer_stock/(?P<bid>[0-9]+)', views.get_beer_stock, name='get_beer_stock'),
    url(r'^beers/get/(?P<bid>[0-9]+)$', views.get_beer, name='get_beer')
)

