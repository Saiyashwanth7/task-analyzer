from django.urls import path
from .views import get_task,add_task,get_sorted_tasks_view
urlpatterns = [
    path('tasks/all_tasks/', get_task,name='get_task'),
    path('tasks/add/',add_task,name='add_task'),
    path('tasks/analyze/',get_sorted_tasks_view,name='get_sorted_tasks'),
]
