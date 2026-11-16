from django.urls import path
from . import lab10_views

urlpatterns = [
    # Part 1: without Django Forms
    path("lab9_part1/listbooks", lab10_views.listbooks_part1, name="lab10_part1_list"),
    path("lab9_part1/addbook", lab10_views.addbook_part1, name="lab10_part1_add"),
    path("lab9_part1/editbook/<int:book_id>", lab10_views.editbook_part1, name="lab10_part1_edit"),
    path("lab9_part1/deletebook/<int:book_id>", lab10_views.deletebook_part1, name="lab10_part1_delete"),

    # Part 2: with Django Forms
    path("lab9_part2/listbooks", lab10_views.listbooks_part2, name="lab10_part2_list"),
    path("lab9_part2/addbook", lab10_views.addbook_part2, name="lab10_part2_add"),
    path("lab9_part2/editbook/<int:book_id>", lab10_views.editbook_part2, name="lab10_part2_edit"),
    path("lab9_part2/deletebook/<int:book_id>", lab10_views.deletebook_part2, name="lab10_part2_delete"),
]
