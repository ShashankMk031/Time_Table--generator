# api/timetable/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('timetable/<int:year>/<int:semester>/<str:branch>/', views.get_timetable, name='get_timetable'),
]
