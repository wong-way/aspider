"""
    urls for symptom
"""

from . import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [

    url(r'^search', views.search),
    url(r'^links', views.links),
    url(r'^list', views.get_disease_list),
    url(r'^newlist', views.get_disease_list2),
    url(r'^statistics', views.get_statistics)
]
