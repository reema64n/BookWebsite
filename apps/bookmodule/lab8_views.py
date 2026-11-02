from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min

from .models import Book
from apps.usermodule.models import Student


def task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, "bookmodule/lab8/task1.html", {"books": books})


def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) &
        (Q(title__icontains="co") | Q(author__icontains="co"))
    )
    return render(request, "bookmodule/lab8/task2.html", {"books": books})


def task3(request):
    # Edition is not higher than 3, and title or authors does not contain "co"
    books = Book.objects.filter(
        Q(edition__lte=3) &
        (~Q(title__icontains="co") | ~Q(author__icontains="co"))
    )
    return render(request, "bookmodule/lab8/task3.html", {"books": books})


def task4(request):
    books = Book.objects.all().order_by("title")
    return render(request, "bookmodule/lab8/task4.html", {"books": books})


def task5(request):
    result = Book.objects.aggregate(
        number_of_books=Count("id"),
        total_price=Sum("price"),
        average_price=Avg("price"),
        maximum_price=Max("price"),
        minimum_price=Min("price"),
    )
    return render(request, "bookmodule/lab8/task5.html", {"result": result})


def task7(request):
    cities = (
        Student.objects.values("address__city")
        .annotate(number_of_students=Count("id"))
        .order_by("address__city")
    )
    return render(request, "bookmodule/lab8/task7.html", {"cities": cities})
