'''
Created on 2014.12.23

@author: Jarvis Zhang
'''

from django.conf.urls import patterns, url
from condor_archive.views import *


urlpatterns = patterns('',
    url(r'^nodeinfo/$', NodeInfoView.as_view()),
    url(r'^transfertime/$', TransferTimeView.as_view()),
    url(r'^transfertime/average/$', TransferTimeAvgView.as_view()),
)
