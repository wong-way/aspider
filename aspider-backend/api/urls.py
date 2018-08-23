from . import views
from django.conf.urls import url

urlpatterns = [
    url('search/(.+)/$', views.search),
    url('links/(.+)/$', views.links)
]
