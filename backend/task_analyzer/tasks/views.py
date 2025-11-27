from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Tasks
from .serializers import TaskSerializer
from .scoring import get_sorted_tasks

# Create your views here.


@api_view(["GET"])
def get_task(request):
    tasks = Tasks.objects.all()
    if tasks is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    tasks_serializer = TaskSerializer(tasks, many=True)
    return Response(tasks_serializer.data)


@api_view(["POST"])
def add_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_sorted_tasks_view(request):
    tasks = Tasks.objects.all()
    tasks_serializer = TaskSerializer(tasks, many=True)
    tasks_data = tasks_serializer.data

    sorted_tasks = get_sorted_tasks(tasks_data)

    return Response(sorted_tasks)

