from django.conf.urls import include, url
from .views import *
from rpc4django.views import serve_rpc_request

urlpatterns = [
    #drawings
    url(r'^get_drawings$', get_drawings),
    #feature reports
    url(r'^wind_report/(\d+)', wind_analysis, name='wind_analysis'), #user requested wind energy site analysis
    url(r'^aoi_report/(\d+)', aoi_analysis, name='aoi_analysis'), #user requested area of interest analysis
    url(r'^rpc$', serve_rpc_request, name='rpc'), #user requested area of interest analysis
]
