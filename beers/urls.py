from django.conf.urls import patterns, url

from beers import views

urlpatterns = patterns('',
    url(r'^search_beer/$', views.search_beer, name='search_beer'),
    url(r'^update_beer/(?P<bid>[0-9]+)/$', views.update_beer, name='update_beer'),
    url(r'^checkout_beer/(?P<bid>[0-9]+)/$', views.checkout_beer, name='checkout_beer'),
    url(r'^stock_index/$', views.stock_index, name='stock_index'),
    url(r'^history_index/$', views.history_index, name='history_index'),
    url(r'^more_history/(?P<page>[0-9]+)/$', views.more_history, name='more_history'),
)