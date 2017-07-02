from django.forms import ModelForm,Textarea
from .models import tb_articles,tb_comments
from django.utils.translation import ugettext_lazy as _
from django import forms
import datetime
import re
import markdown

class ArticlePublishForm(ModelForm):
    class Meta:
        model=tb_articles
        exclude=["articleID","content_html","created","updated"]
        labels={
            'title':_('文章标题'),
            'content_md':_('文章内容'),
            'tagID':_('文章分类'),
        }
        widgets={
            'abstract':Textarea(attrs={'cols':30,'rows':5}),
        }
    def save(self,username):
        cd=self.cleaned_data
        title=cd['title']
        content_md=cd['content_md']
        content_html=markdown.markdown(cd['content_md'])
        tag=cd['tagID']
        abstract=cd['abstract']
        created=datetime.datetime.now()
        updated=datetime.datetime.now()
        article=tb_articles(title=title,content_md=content_md,content_html=content_html,abstract=abstract,tagID=tag,created=created,updated=updated)
        article.save()
        
class ArticleEditForm(ModelForm):
    class Meta:
        model=tb_articles
        exclude=['articleID','content_html','created','updated']
        labels={
            'title':_('文章标题'),
            'content_md':_('文章内容'),
            'tagID':_('文章分类'),
        }
        widgets={
            'abstract':Textarea(attrs={'cols':30,'rows':5}),
        }
    def save(self,username,article=None):
        cd=self.cleaned_data
        title=cd['title']
        abstract=cd['abstract']
        content_md=cd['content_md']
        content_html=markdown.markdown(cd['content_md'])
        tagID=cd['tagID']
        if article:
            article.title=title
            article.abstract=abstract
            article.content_md=content_md
            article.content_html=content_html
            article.tagID=tagID
            article.updated=datetime.datetime.now()
        else:
            article=tb_articles(
            title=title,
            content_md=content_md,
            content_html=content_html,
            abstract=abstract,
            tagID=tagID,
            created=datetime.datetime.now(),
            updated=datetime.datetime.now()
            )
        article.save()

class CommentForm(ModelForm):
    class Meta:
        model=tb_comments
        fields=['content']
    def save(self,IP,articleID):
        cd=self.cleaned_data
        content=cd['content']
        lefted=datetime.datetime.now()
        comment=tb_comments(articleID=articleID,content=content,IP=IP,lefted=lefted)
        comment.save()

class ProjForm(forms.Form):
    title=forms.CharField(max_length=24)
    abstract=forms.CharField(max_length=140)
    gitURL=forms.URLField()
    img1=forms.ImageField()
    img2=forms.ImageField()
    img3=forms.ImageField()
    img4=forms.ImageField()
    img5=forms.ImageField()
