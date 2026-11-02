from django.shortcuts import render
from django.db.models import (
    Sum, Min, Max, Avg, Count, Q, F, Value,
    FloatField, ExpressionWrapper, Subquery, OuterRef
)
from django.db.models.functions import Coalesce

from .models import Book, Publisher

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, "bookmodule/list_books.html")

def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")

def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def html5_links(request):
    return render(request, 'bookmodule/html5/links.html')


def html5_formatting(request):
    return render(request, 'bookmodule/html5/formatting.html')


def html5_listing(request):
    return render(request, 'bookmodule/html5/listing.html')


def html5_tables(request):
    return render(request, 'bookmodule/html5/tables.html')

def __getBooksList():
    book1 = {
        'id': 12344321,
        'title': 'Continuous Delivery',
        'author': 'J.Humble and D. Farley'
    }
    book2 = {
        'id': 56788765,
        'title': 'Reversing: Secrets of Reverse Engineering',
        'author': 'E. Eilam'
    }
    book3 = {
        'id': 43211234,
        'title': 'The Hundred-Page Machine Learning Book',
        'author': 'Andriy Burkov'
    }
    return [book1, book2, book3]


def search_books(request):
    # فتح صفحة البحث لأول مرة (GET)
    if request.method == "GET":
        return render(request, 'bookmodule/search.html')

    # معالجة الاستمارة بعد الضغط على Search (POST)
    keyword = request.POST.get('keyword', '').strip()
    search_title = request.POST.get('option1') is not None
    search_author = request.POST.get('option2') is not None

    books = __getBooksList()
    new_books = []

    # يجب تحديد Title أو Author حتى نعرف أين نبحث
    if search_title or search_author:
        search_text = keyword.lower()

        for item in books:
            contained = False

            if search_title and search_text in item['title'].lower():
                contained = True

            if search_author and search_text in item['author'].lower():
                contained = True

            if contained:
                new_books.append(item)

    # نعرض صفحة النتائج مع الاحتفاظ ببيانات البحث
    return render(
        request,
        'bookmodule/bookList.html',
        {
            'books': new_books,
            'keyword': keyword,
            'search_title': search_title,
            'search_author': search_author,
        }
    )

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/lab7_bookList.html', {'books': mybooks})


def complex_query(request):
    mybooks = (
        Book.objects
        .filter(author__isnull=False)
        .filter(title__icontains='and')
        .filter(edition__gte=2)
        .exclude(price__lte=100)[:10]
    )

    if mybooks.exists():
        return render(request, 'bookmodule/lab7_bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    
def lab9_task1(request):
    total_quantity = Book.objects.aggregate(total=Sum('quantity'))['total'] or 0

    if total_quantity > 0:
        books = Book.objects.annotate(
            availability_percentage=ExpressionWrapper(
                F('quantity') * Value(100.0) / Value(float(total_quantity)),
                output_field=FloatField()
            )
        )
    else:
        books = Book.objects.annotate(
            availability_percentage=Value(0.0, output_field=FloatField())
        )

    return render(request, 'bookmodule/lab9/task1.html', {
        'books': books,
        'total_quantity': total_quantity
    })


def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_stock=Coalesce(Sum('books__quantity'), 0)
    )
    return render(request, 'bookmodule/lab9/task2.html', {
        'publishers': publishers
    })


def lab9_task3(request):
    oldest_book = Book.objects.filter(
        publisher=OuterRef('pk')
    ).order_by('pubdate')

    publishers = Publisher.objects.annotate(
        oldest_book_title=Subquery(oldest_book.values('title')[:1]),
        oldest_book_date=Min('books__pubdate')
    )
    return render(request, 'bookmodule/lab9/task3.html', {
        'publishers': publishers
    })


def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        average_price=Avg('books__price'),
        minimum_price=Min('books__price'),
        maximum_price=Max('books__price')
    )
    return render(request, 'bookmodule/lab9/task4.html', {
        'publishers': publishers
    })


def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count(
            'books',
            filter=Q(books__rating__gte=4)
        )
    )

    # لإظهار أسماء الكتب ذات التقييم المرتفع وكمياتها بجانب كل ناشر.
    for publisher in publishers:
        publisher.high_rated_books = Book.objects.filter(
            publisher=publisher,
            rating__gte=4
        ).values('title', 'quantity')

    return render(request, 'bookmodule/lab9/task5.html', {
        'publishers': publishers
    })


def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        matching_books_count=Count(
            'books',
            filter=Q(
                books__price__gt=50,
                books__quantity__lt=5,
                books__quantity__gte=1
            )
        )
    )
    return render(request, 'bookmodule/lab9/task6.html', {
        'publishers': publishers
    })

    
    

