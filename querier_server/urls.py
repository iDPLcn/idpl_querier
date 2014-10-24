'''
Created on 2014.10.23

@author: Jarvis Zhang
'''

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^throughput/$', views.ThroughputQuerier.as_view()),
)