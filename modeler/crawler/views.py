from django.shortcuts import render
from .models import Resource
import crawlers
 
def index(request):
    return render(request, "crawler/index.html")

def exec_crawler():
    resources = Resource.objects.all()
    for res in resources:
        getattr(crawlers, res.name)()
