import uuid
from django.db import models

# Create your models here:


class tb_tags(models.Model):
    name=models.CharField(max_length=24,verbose_name="分类")
    articlecount=models.PositiveIntegerField(verbose_name="同类文章数量")
    id=models.PositiveIntegerField(primary_key=True,verbose_name="正则id")
    
    def __str__(self):
        return str(self.name)

class tb_articles(models.Model):
    articleID=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,verbose_name="文章ID")
    title=models.CharField(max_length=30,db_index=True,verbose_name='标题')
    content_md=models.TextField(verbose_name='Markdown内容')
    content_html=models.TextField(verbose_name='html内容')
    abstract=models.CharField(max_length=140,verbose_name='摘要')
    tagID=models.ForeignKey(tb_tags,on_delete=models.CASCADE)
    created=models.DateTimeField(verbose_name='创建时间')
    updated=models.DateTimeField(verbose_name='更新时间')
    
    def __str__(self):
        return str(self.articleID)

class tb_comments(models.Model):
    articleID=models.ForeignKey(tb_articles,on_delete=models.CASCADE)
    commentID=models.AutoField(primary_key=True,verbose_name="留言ID")
    content=models.CharField(max_length=140,verbose_name="留言内容")
    IP=models.CharField(max_length=30,verbose_name="留言来源")
    lefted=models.DateTimeField(verbose_name="留言时间")


class tb_projs(models.Model):
    projID=models.AutoField(primary_key=True,verbose_name="作品ID")
    title=models.CharField(max_length=24,db_index=True,verbose_name="作品名")
    abstract=models.CharField(max_length=140,verbose_name="作品简介")
    uploaded=models.DateTimeField(verbose_name="作品发布时间")
    imgsURL=models.URLField(verbose_name="作品图集")
    gitURL=models.URLField(default="github.com/HitBirds",verbose_name="作品GitHubURL")
