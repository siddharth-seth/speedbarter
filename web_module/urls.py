from django.conf.urls import patterns, url
from web_module import views
from web_module.accounts.views import *

__author__ = 'Anant'


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^account/login/$', account_login, name='login'),
                       url(r'^account/logout/$', account_logout, name='logout'),
)