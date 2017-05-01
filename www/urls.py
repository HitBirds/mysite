from django.conf.urls import url
from . import views
app_name= 'www'
urlpatterns=[
    url(r'^$',views.indexView,name='indexView'),
    url(r'^(?P<filter>[0-9]+)/(?P<page>[0-9]+)/$',views.ArticleListView.as_view(),name="articleList"),
]
