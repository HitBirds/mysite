from django.shortcuts import render

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import *
from django.db.models import F
from django.views.generic import ListView

from django.http import Http404
from django.views.generic.detail import DetailView

from .forms import *
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from .auths import *
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

class ArticleDetailView(DetailView):
    template_name="www/article_detail_base.html"
    context_object_name="article"
    
    def get_object(self,**kwargs):
        artId=self.kwargs.get('article')
        try:
            art=tb_articles.objects.get(articleID=artId)
        except tb_articles.DoesNotExist:
            raise Http404("Article does not exist")
        return art

    def get_context_data(self,**kwargs):
        context=super(ArticleDetailView,self).get_context_data(**kwargs)
        artId=self.kwargs.get('article')
        artDate=tb_articles.objects.get(articleID=artId).created
        context['comments']=tb_comments.objects.filter(articleID=artId).order_by(F('lefted').desc())
        try:
            context['nextID']=tb_articles.objects.raw('''
                                          select articleID from www_tb_articles
                                          where created < %s
                                          order by created desc limit 1''',[artDate])[0].articleID
        except:
            context['nextID']="#"
        try:
            context['prevID']=tb_articles.objects.raw('''
                                          select articleID from www_tb_articles
                                          where created >%s
                                          order by created asc limit 1''',[artDate])[0].articleID
        except:
            context['prevID']="#"
        return context

class ArticlePublishView(Staff_test,FormView):
    template_name="www/article_publish_base.html"
    form_class=ArticlePublishForm
    success_url='blogs/0/1'
    def form_valid(self,form):
        form.save(self.request.user.username)
        return super(ArticlePublishView,self).form_valid(form)
    
class ArticleEditView(FormView):
    template_name="www/article_edit_base.html"
    form_class=ArticleEditForm
    article=None
    def get_initial(self,**kwargs):
        artID=self.kwargs.get('article')
        try:
            self.article=tb_articles.objects.get(articleID=artID)
            initial={
                'title':self.article.title,
                'abstract':self.article.abstract,
                'content_md':self.article.content_md,
                'tagID':self.article.tagID,
            }
            return initial
        except tb_article.DoesNotExist:
            raise Http404("Article does not exist")
    
    def form_valid(self,form):
        form.save(self.request.user.username,self.article)
        return super(ArticleEditView,self).form_valid(form)

    def get_success_url(self):
        l_uuid=str(self.article.articleID).split('-')
        s_uuid=''.join(l_uuid)
        success_url=reverse('www:articleDetail',kwargs={'filter':0,'article':s_uuid})
        return success_url
