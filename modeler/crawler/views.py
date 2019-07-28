from django.shortcuts import render
from .models import Resource
from crawler import crawlers

def index(request):
    exec_crawler()
    return render(request, "crawler/index.html")

def exec_crawler():
    print("exec_crawler")
    resources = Resource.objects.all()
    for res in resources:
        getattr(crawlers, res.name)(res.url)
