from django.conf.urls import patterns, include, url
# from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'idpl_querier.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#     url(r'^admin/', include(admin.site.urls)),
    url(r'^perfsonar/', include('querier_server.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
