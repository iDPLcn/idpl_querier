'''
Created on 2014.10.23

@author: Jarvis Zhang
'''

from django.conf.urls import patterns, url
from querier_server.views import ThroughputQuerier


urlpatterns = patterns('',
    url(r'^throughput/$', ThroughputQuerier.as_view()),
)