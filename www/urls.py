from django.contrib.auth import views as auth_views
from django.conf.urls import url,include
from . import views


app_name= 'www'
urlpatterns=[
    url('^',include('django.contrib.auth.urls')),
    url(r'^$',views.indexView,name='indexView'),
    url(r'^(?P<filter>[0-9]+)/(?P<page>[0-9]+)/$',views.ArticleListView.as_view(),name="articleList"),
    url(r'^(?P<filter>[0-9]+)/article/(?P<article>\w+)/$',views.ArticleDetailView.as_view(),name="articleDetail"),
    url(r'^article/publish/$',views.ArticlePublishView.as_view(),name="articlePublish"),
    url(r'^article/edit/(?P<article>\w+)/$',views.ArticleEditView.as_view(),name="articleEdit"),
]
