from django.shortcuts import render

from .models import *
# Create your views here.
def indexView(request):
    return render(request,'www/index_base.html',{})
