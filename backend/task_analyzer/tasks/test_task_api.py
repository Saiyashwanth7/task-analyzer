import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta


@pytest.fixture
def api_client():
    """Fixture to create an API client for testing"""
    return APIClient()

#Similar to client=TestCilent() in FastAPI, but it uses it as a fixture

@pytest.fixture
def sample_task_data():
    """Fixture with sample task data"""
    tomorrow = date.today() + timedelta(days=1)
    #This task is a mock task. It is not saved to the database yet.
    return {
        "title": "Complete project documentation",
        "due_date": tomorrow.strftime("%Y-%m-%d"),
        "estimated_hours": 3.5,
        "importance": 8,
        "dependencies": "",
        "completed": False
    }


@pytest.mark.django_db
def test_add_task(api_client, sample_task_data):
    """Test creating a new task via POST /tasks/add/"""
    
    #this add_task is a function from views.py, which is mapped to the api get endpoitnt /tasks/add/
    url = reverse('add_task') 
    #This response will contain the response from the API after posting the sample task data.
    response = api_client.post(url, sample_task_data, format='json')
    #This response is a response object which contains all the data from the task (simple task in this case)
    # and the status code of the response.
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == sample_task_data['title']
    assert response.data['importance'] == sample_task_data['importance']
    assert response.data['completed'] is False
    assert 'id' in response.data


@pytest.mark.django_db
def test_get_all_tasks(api_client, sample_task_data):
    """Test retrieving all tasks via GET /tasks/all_tasks/"""
    # First, create a task
    add_url = reverse('add_task')
    api_client.post(add_url, sample_task_data, format='json')
    
    # Then retrieve all tasks
    get_url = reverse('get_task') #the get_task is mapped to /tasks/all_tasks/ endpoint in views.py
    response = api_client.get(get_url)
    # the response.data will contain a list of all tasks in the database in general. But, it only contains the sample task data here
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    assert response.data[0]['title'] == sample_task_data['title']


@pytest.mark.django_db
def test_analyze_tasks_with_strategy(api_client, sample_task_data):
    """Test task prioritization via GET /tasks/analyze/ with different strategies"""
    # Create two tasks with different priorities
    add_url = reverse('add_task')
    # In this below line, we will create duplicate of sample_task_data but change the title and importance to populate the tasks list with different tasks
    task1 = {**sample_task_data, "title": "Urgent task", "importance": 9}
    api_client.post(add_url, task1, format='json') 
    # this is anothe duplicate of sample_task_data with changes in different fields
    task2 = {
        **sample_task_data, 
        "title": "Low priority task",
        "importance": 3,
        "due_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
    }
    api_client.post(add_url, task2, format='json') #Adding the second task 

    analyze_url = reverse('get_sorted_tasks') # the get_sorted_tasks is mapped to /tasks/analyze/ endpoint in views.py
    # here we are passing strategy as query parameter in the get request ,{'strategy': 'Smart Balance'} is how we pass query parameters in DRF test client
    response = api_client.get(analyze_url, {'strategy': 'Smart Balance'})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert 'priority_score' in response.data[0]
    assert 'priority_explanation' in response.data[0]
    
    assert response.data[0]['title'] == "Urgent task"
    assert response.data[0]['priority_score'] > response.data[1]['priority_score']