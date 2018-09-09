from django.conf.urls import url

from disease import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^searchDisease$', views.search_disease),
    url(r'^searchGene$', views.search_relate_gene),
    url(r'^searchInheri$', views.search_inheri),
    url(r'^searchSymptom$', views.search_symptom),
    url(r'^searchSimilar$', views.search_similar),
    url(r'^search', views.search),
    url(r'^links', views.links),

    # huangwei
    url(r'^detail', views.get_detail),
    url(r'^list', views.get_disease_list),
    url(r'^newlist', views.get_disease_list2),
    url(r'^statistics', views.get_statistics),
    url(r'^top5item', views.get_top5item),
    url(r'^graph', views.get_graph),
    url(r'^test', views.node_test),
    url(r'^link', views.get_link_of_disease),


]
