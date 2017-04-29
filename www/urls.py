from django.conf.urls import url
from . import views
app_name= 'www'
urlpatterns=[
    url(r'^$',views.indexView,name='indexView'),
]
