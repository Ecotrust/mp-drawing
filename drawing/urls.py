# from django.conf.urls import url, patterns
from django.urls import re_path, include
from drawing.views import *
from rpc4django.views import serve_rpc_request

urlpatterns = [
    #'',
    #drawings
    re_path(r'^get_drawings$', get_drawings),
    #feature reports
    re_path(r'^wind_report/(\d+)', wind_analysis, name='wind_analysis'), #user requested wind energy site analysis
    re_path(r'^aoi_report/(\d+)', aoi_analysis, name='aoi_analysis'), #user requested area of interest analysis
    re_path(r'^rpc$', serve_rpc_request, name='rpc'), #user requested area of interest analysis
    re_path(r'get_attributes/(?P<uid>[\w_]+)/$', get_attributes), #get attributes for a given scenario
]
