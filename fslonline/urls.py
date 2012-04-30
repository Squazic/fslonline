from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fslonline.views.home', name='home'),
    # url(r'^fslonline/', include('fslonline.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^fsl/$', 'fsl.views.home'),
    url(r'^fsl/(?P<file_name>[a-zA-Z0-9\._]+)/$', 'fsl.views.run_fsl'),
    url(r'^fsl/(?P<file_name>[a-zA-Z0-9\._]+)/(?P<num>\d+)$', 'fsl.views.disp_fsl'),
    url(r'^admin/', include(admin.site.urls)),

    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
