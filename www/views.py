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
        paginator=Paginator(queryset,10)
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)
        for obj in queryset:
            obj.articleID=''.join(str(obj.articleID).split('-'))
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
        context['artId']=artId
        context['comments']=tb_comments.objects.filter(articleID=artId).order_by(F('lefted').desc())
        try:
            art=tb_articles.objects.raw('''
                                          select articleID,title from www_tb_articles
                                          where created < %s
                                          order by created desc limit 1''',[artDate])[0]
            context['nextID']=art.articleID
            context['nextID']=''.join(str(context['nextID']).split('-'))
            context['nextTitle']=art.title
        except:
            context['nextID']="#"
            context['nextTitle']="没有啦"
        try:
            art=tb_articles.objects.raw('''
                                          select articleID,title from www_tb_articles
                                          where created >%s
                                          order by created asc limit 1''',[artDate])[0]
            context['prevID']=art.articleID
            context['prevID']=''.join(str(context['prevID']).split('-'))
            context['prevTitle']=art.title
        except:
            context['prevID']="#"
            context['prevTitle']="没有啦"
        return context

class ArticlePublishView(Staff_test,FormView):
    template_name="www/article_publish_base.html"
    form_class=ArticlePublishForm
    success_url='blogs/0/1'
    def form_valid(self,form):
        form.save(self.request.user.username)
        return super(ArticlePublishView,self).form_valid(form)
    
class ArticleEditView(Staff_test,FormView):
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

class CommentPubView(FormView):
    form_class=CommentForm
    template_name="www/comment_plugin.html"
    ip=None
    artID=None
    def get_initial(self,**kwargs):
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            self.ip=self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            self.ip=self.request.META['REMOTE_ADDR']
        artID=self.kwargs.get('article')
        self.artID=tb_articles.objects.get(articleID=artID)


    def form_valid(self,form):
        form.save(self.ip,self.artID)
        return super(CommentPubView,self).form_valid(form)

    def get_success_url(self):
        l_uuid=str(self.kwargs.get('article')).split('-')
        s_uuid=''.join(l_uuid)
        success_url=reverse('www:articleDetail',kwargs={'filter':0,'article':s_uuid})
        return  success_url

class ProjListView(ListView):
    template_name="www/projList_base.html"
    model=tb_projs
    context_object_name="projs"
    def get_context_data(self,**kwargs):
        """
        Return context data for displaying the list of objects
        """
        context=super(ProjListView,self).get_context_data(**kwargs)
        return context

class ProjPublishView(Staff_test,FormView):
    template_name="www/proj_publish_base.html"
    form_class=ProjForm
    absolute_path='/virEnv/mysite/www/static/' 
    def form_valid(self,form):
        if form.is_valid():
            data=form.cleaned_data
            title=data['title']
            abstract=data['abstract']
            uploaded=datetime.datetime.now()
            gitURL=data['gitURL']
            imgsURL='www/projImgs'
            proj=tb_projs(title=title,abstract=abstract,uploaded=uploaded,imgsURL=imgsURL,gitURL=gitURL)
            proj.save()
            img1_path=self.absolute_path+imgsURL+'/'+str(proj.projID)+'_1.jpg'
            self.handle_uploaded_img(self.request.FILES['img1'],img1_path)
            img2_path=self.absolute_path+imgsURL+'/'+str(proj.projID)+'_2.jpg'
            self.handle_uploaded_img(self.request.FILES['img2'],img2_path)
            img3_path=self.absolute_path+imgsURL+'/'+str(proj.projID)+'_3.jpg'
            self.handle_uploaded_img(self.request.FILES['img3'],img3_path)
            img4_path=self.absolute_path+imgsURL+'/'+str(proj.projID)+'_4.jpg'
            self.handle_uploaded_img(self.request.FILES['img4'],img4_path)
            img5_path=self.absolute_path+imgsURL+'/'+str(proj.projID)+'_5.jpg'
            self.handle_uploaded_img(self.request.FILES['img5'],img5_path)
        return super(ProjPublishView,self).form_valid(form)

    def handle_uploaded_img(self,f,path):
        with open(path,'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get_success_url(self):
        #success_url=reverse('www:projList',kwargs={'page':1})
        success_url=reverse('www:indexView')
        return success_url

class ProjDetailView(DetailView):
    template_name="www/projDetail_base.html"
    context_object_name="project"
    model=tb_projs
    def get_object(self,**kwargs):
        projID=self.kwargs.get('projID')
        try:
            project=tb_projs.objects.get(projID=projID)
        except tb_projs.DoesNotExist:
            raise Http404("Project does not exist")
        return project

    def get_context_data(self,**kwargs):
        context=super(ProjDetailView,self).get_context_data(**kwargs)
        return context
