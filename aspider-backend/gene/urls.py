from django.conf.urls import url
from gene import views

urlpatterns = [
    # 旧路由
    url(r'^index$', views.index),
    # url(r'^search$', views.search_gene),
    url(r'^link$', views.search_relation_disease),
    url(r'^link2$', views.search_relation_gene),

    # 新的路由
    url(r'^search', views.search),
    url(r'^links', views.links),
    url(r'^list', views.get_disease_list),
    url(r'^newlist', views.get_disease_list2),
    url(r'^statistics', views.get_statistics)

]
