from django.forms import ModelForm,Textarea
from .models import tb_articles
from django.utils.translation import ugettext_lazy as _
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
