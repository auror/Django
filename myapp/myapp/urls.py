from django.conf.urls import patterns, include, url
#from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$', 'rlp.views.login_user'),
    (r'^chat/$', 'rlp.views.chatFunc'),
    url(r'^admin/', include(admin.site.urls)),
)
