from django.conf.urls import url

from common import views

urlpatterns = [
    url(r'^disease_info$', views.get_disease_info),
    url(r'^inheri_info$', views.get_inheritance_info),
]
