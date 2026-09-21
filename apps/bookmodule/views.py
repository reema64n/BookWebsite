from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    name = request.GET.get("name")
    return render(request, "index.html" , {"name": name})

def index2(request, val1):
    return HttpResponse(f"Value is {val1}")

def viewbook(request):
    books = [
        "Python Programming",
        "Django for Beginners",
        "Web Technologies",
        "Artificial Intelligence"
    ]
    return render(request, "show.html", {"books": books})
