from django.shortcuts import render

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import *
from django.db.models import F
from django.views.generic import ListView
# Create your views here.
def indexView(request):
    return render(request,'www/index_base.html',{})

class ArticleListView(ListView):
    context_object_name='articles'
    template_name="www/articleList_base.html"
    
    def get_queryset(self,**kwargs):
        ID=int(self.kwargs.get('filter'))
        page=self.kwargs.get('page')
        if ID<=0:
            queryset=tb_articles.objects.all().order_by(F('created').desc())[:100]
        else: 
            queryset=tb_articles.objects.filter(tagID__id=ID).order_by(F('created').desc())[:100]
        paginator=Paginator(queryset,1)
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)
        return queryset

    def get_context_data(self,**kwargs):
        context=super(ArticleListView,self).get_context_data(**kwargs)
        context['myfilter']=self.kwargs.get('filter')
        context['filters']=tb_tags.objects.all()
        return context
