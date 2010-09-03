from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/', 'django.contrib.auth.views.login'),
    (r'^admin/', include(admin.site.urls)),
)
