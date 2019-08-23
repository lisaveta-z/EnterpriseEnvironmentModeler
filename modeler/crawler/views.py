from django.shortcuts import render
from crawler import crawlers_executor

def index(request):
    #crawlers_executor.exec_crawler()
    return render(request, "crawler/index.html")
