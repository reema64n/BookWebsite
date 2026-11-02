from django.urls import path
from . import lab8_views

urlpatterns = [
    path("task1", lab8_views.task1, name="lab8_task1"),
    path("task2", lab8_views.task2, name="lab8_task2"),
    path("task3", lab8_views.task3, name="lab8_task3"),
    path("task4", lab8_views.task4, name="lab8_task4"),
    path("task5", lab8_views.task5, name="lab8_task5"),
    path("task7", lab8_views.task7, name="lab8_task7"),
]
