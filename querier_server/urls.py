'''
Created on 2014.10.23

@author: Jarvis Zhang
'''

from django.conf.urls import patterns, url
from querier_server.views import NetworkQuerier, ThroughputQuerier, OwdelayQuerier


urlpatterns = patterns('',
    url(r'^throughput/$', ThroughputQuerier.as_view()),
    url(r'^owdelay/$', OwdelayQuerier.as_view()),
    url(r'^query/$', NetworkQuerier.as_view()),
)