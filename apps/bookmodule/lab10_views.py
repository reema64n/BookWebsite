from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils import timezone
from .models import Book
from .lab10_forms import BookModelForm


def _list_context(part):
    if part == "part1":
        return {
            "part": part,
            "add_url_name": "lab10_part1_add",
            "edit_url_name": "lab10_part1_edit",
            "delete_url_name": "lab10_part1_delete",
            "heading": "Books - Part 1 (Without Django Forms)",
        }
    return {
        "part": part,
        "add_url_name": "lab10_part2_add",
        "edit_url_name": "lab10_part2_edit",
        "delete_url_name": "lab10_part2_delete",
        "heading": "Books - Part 2 (Using Django Forms)",
    }


def _list_books(request, part):
    context = _list_context(part)
    context["books"] = Book.objects.all().order_by("pk")
    return render(request, "bookmodule/lab10/listbooks.html", context)


# -----------------------------
# Part 1: CRUD without Django Forms
# -----------------------------

def listbooks_part1(request):
    return _list_books(request, "part1")


def _raw_form_fields(book=None):
    """Build HTML input descriptions from the actual Book model fields."""
    result = []
    for field in Book._meta.fields:
        if field.primary_key or field.auto_created:
            continue
        if field.is_relation:
            continue

        if isinstance(field, models.DateTimeField):
            input_type = "datetime-local"
        elif isinstance(field, models.DateField):
            input_type = "date"
        elif isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
            input_type = "number"
        elif isinstance(field, models.BooleanField):
            input_type = "checkbox"
        else:
            input_type = "text"

        value = ""
        checked = False
        if book is not None:
            value = getattr(book, field.name, "")
            if isinstance(field, models.DateTimeField) and value:
                if timezone.is_aware(value):
                    value = timezone.localtime(value)
                value = value.strftime("%Y-%m-%dT%H:%M")
            elif isinstance(field, models.DateField) and value:
                value = value.strftime("%Y-%m-%d")
            elif isinstance(field, models.BooleanField):
                checked = bool(value)
            elif value is None:
                value = ""
        elif field.has_default():
            value = field.get_default()
            if isinstance(field, models.DateTimeField) and value:
                value = value.strftime("%Y-%m-%dT%H:%M")

        result.append({
            "name": field.name,
            "label": field.verbose_name.capitalize(),
            "type": input_type,
            "value": value,
            "checked": checked,
            "required": not field.blank and not field.null and not field.has_default(),
        })
    return result


def _raw_related_fields(book=None):
    foreign_fields = []
    many_fields = []

    for field in Book._meta.get_fields():
        if not getattr(field, "is_relation", False):
            continue
        if field.auto_created:
            continue
        if field.many_to_many:
            selected_ids = list(getattr(book, field.name).values_list("pk", flat=True)) if book else []
            many_fields.append({
                "name": field.name,
                "label": field.verbose_name.capitalize(),
                "options": field.related_model.objects.all(),
                "selected_ids": selected_ids,
            })
        elif field.concrete is False:
            continue
        elif field.many_to_one or field.one_to_one:
            selected = getattr(book, field.name, None) if book else None
            foreign_fields.append({
                "name": field.name,
                "label": field.verbose_name.capitalize(),
                "options": field.related_model.objects.all(),
                "selected": selected.pk if selected else None,
                "required": not field.blank and not field.null,
            })
    return foreign_fields, many_fields


def _raw_form_context(book=None, errors=None, is_edit=False):
    foreign_fields, many_fields = _raw_related_fields(book)
    return {
        "use_django_form": False,
        "raw_fields": _raw_form_fields(book),
        "foreign_fields": foreign_fields,
        "many_fields": many_fields,
        "errors": errors or [],
        "is_edit": is_edit,
        "book": book,
        "cancel_url_name": "lab10_part1_list",
    }


def _save_raw_book(request, book=None):
    """Read POST values directly and save the Book without using Django forms."""
    if book is None:
        book = Book()

    many_to_many_values = {}

    for field in Book._meta.fields:
        if field.primary_key or field.auto_created:
            continue

        if field.is_relation:
            raw_value = request.POST.get(field.name, "").strip()
            if raw_value:
                related_object = field.related_model.objects.get(pk=raw_value)
                setattr(book, field.name, related_object)
            elif field.null or field.blank:
                setattr(book, field.name, None)
            continue

        if isinstance(field, models.BooleanField):
            raw_value = request.POST.get(field.name) == "on"
        elif field.name in request.POST:
            raw_value = request.POST.get(field.name)
        elif field.has_default() and book.pk is None:
            continue
        elif field.blank:
            raw_value = ""
        else:
            continue

        setattr(book, field.name, field.to_python(raw_value))

    for field in Book._meta.many_to_many:
        if field.name in request.POST:
            many_to_many_values[field.name] = request.POST.getlist(field.name)
        else:
            many_to_many_values[field.name] = []

    book.full_clean()
    book.save()

    for field_name, ids in many_to_many_values.items():
        getattr(book, field_name).set(ids)

    return book


def addbook_part1(request):
    if request.method == "POST":
        try:
            _save_raw_book(request)
            return redirect("lab10_part1_list")
        except (ValidationError, ValueError, TypeError, ObjectDoesNotExist) as exc:
            errors = exc.messages if isinstance(exc, ValidationError) else [str(exc)]
            return render(
                request,
                "bookmodule/lab10/book_form.html",
                {**_raw_form_context(errors=errors), "page_title": "Add a book"},
            )

    return render(
        request,
        "bookmodule/lab10/book_form.html",
        {**_raw_form_context(), "page_title": "Add a book"},
    )


def editbook_part1(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        try:
            _save_raw_book(request, book)
            return redirect("lab10_part1_list")
        except (ValidationError, ValueError, TypeError, ObjectDoesNotExist) as exc:
            errors = exc.messages if isinstance(exc, ValidationError) else [str(exc)]
            return render(
                request,
                "bookmodule/lab10/book_form.html",
                {**_raw_form_context(book, errors, True), "page_title": "Edit book"},
            )

    return render(
        request,
        "bookmodule/lab10/book_form.html",
        {**_raw_form_context(book, is_edit=True), "page_title": "Edit book"},
    )


def deletebook_part1(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("lab10_part1_list")
    return render(
        request,
        "bookmodule/lab10/delete_confirm.html",
        {"book": book, "cancel_url_name": "lab10_part1_list"},
    )


# -----------------------------
# Part 2: CRUD with Django Forms
# -----------------------------

def listbooks_part2(request):
    return _list_books(request, "part2")


def addbook_part2(request):
    if request.method == "POST":
        form = BookModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lab10_part2_list")
    else:
        form = BookModelForm()

    return render(
        request,
        "bookmodule/lab10/book_form.html",
        {
            "use_django_form": True,
            "form": form,
            "page_title": "Add a book (Django Form)",
            "cancel_url_name": "lab10_part2_list",
        },
    )


def editbook_part2(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookModelForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("lab10_part2_list")
    else:
        form = BookModelForm(instance=book)

    return render(
        request,
        "bookmodule/lab10/book_form.html",
        {
            "use_django_form": True,
            "form": form,
            "page_title": "Edit book (Django Form)",
            "cancel_url_name": "lab10_part2_list",
        },
    )


def deletebook_part2(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("lab10_part2_list")
    return render(
        request,
        "bookmodule/lab10/delete_confirm.html",
        {"book": book, "cancel_url_name": "lab10_part2_list"},
    )
