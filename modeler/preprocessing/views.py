from django.shortcuts import render
from preprocessing import preprocessing_v2

def index(request):
    preprocessing_v2.preprocessing()
    return render(request, "crawler/index.html")
