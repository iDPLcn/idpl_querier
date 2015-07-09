'''
Created on 2014.12.23

@author: Jarvis Zhang
'''

from django.conf.urls import patterns, url
from condor_archive.views import *


urlpatterns = patterns('',
    url(r'^nodeinfo/$', NodeInfoView.as_view()),
    url(r'^measurementinfo/$', MeasurementInfoView.as_view()),
    url(r'^measuremenetdata/$', MeasurementDataView.as_view()),
    url(r'^measuremenetdata/average/$', MeasurementDataAvgView.as_view()),
    url(r'^measurepair/', MeasurePairView.as_view()),
    url(r'^transfertime/$', TransferTimeView.as_view()),
    url(r'^transfertime/average/$', TransferTimeAvgView.as_view()),
    url(r'^iperftime/$', IperfTimeView.as_view()),
    url(r'^iperftime/average/$', IperfTimeAvgView.as_view()),
    url(r'^netcatdata/$', NetcatDataView.as_view()),
    url(r'^netcatdata/average/$', NetcatDataAvgView.as_view()),
)
