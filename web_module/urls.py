from django.conf.urls import patterns, url
from web_module import views
__author__ = 'Anant'


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
)