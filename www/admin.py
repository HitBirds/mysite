from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(tb_articles)
admin.site.register(tb_tags)
admin.site.register(tb_comments)
admin.site.register(tb_projs)
