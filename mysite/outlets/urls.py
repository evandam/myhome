from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/$', views.list, name='api_list'),
    url(r'^api/(?P<outlet_id>\d+)/on$', views.turn_on, name='outlet_on'),
    url(r'^api/(?P<outlet_id>\d+)/off$', views.turn_off, name='outlet_off'),
]
