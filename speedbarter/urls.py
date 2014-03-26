from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'', include('web_module.urls', namespace='web_module')),
                       url(r'^admin/', include(admin.site.urls)),
)
