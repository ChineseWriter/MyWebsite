# coding = UTF-8


from django.shortcuts import render


def index(request):
    return render(request, "MyWebsite/index.html")
