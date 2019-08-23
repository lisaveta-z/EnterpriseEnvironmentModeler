from django.shortcuts import render
from preprocessing import preprocessing

def index(request):
    preprocessing.preprocessing()
    return render(request, "crawler/index.html")
