# api/timetable/views.py
from django.http import JsonResponse
from django.conf import settings  # Import settings to access project root
import os
from core.utils import load_courses, load_faculties, load_classrooms, load_sections, load_time_slots

def get_timetable(request, year, semester, branch):
    """
    Returns the timetable data as JSON for the given year, semester, and branch.
    For now, we will just load all the initial data.
    """
    BASE_DIR = settings.BASE_DIR.parent.parent  # Get to the root 'timetable_generator' directory
    data_dir = os.path.join(BASE_DIR, 'data')

    courses = load_courses(os.path.join(data_dir, 'courses.json'))
    faculties = load_faculties(os.path.join(data_dir, 'faculties.json'))
    classrooms = load_classrooms(os.path.join(data_dir, 'classrooms.json'))
    sections = load_sections(os.path.join(data_dir, 'sections.json'))
    time_slots = load_time_slots(os.path.join(data_dir, 'time_slots.json'))

    timetable_data = {
        'year': year,
        'semester': semester,
        'branch': branch,
        'courses': [course.__dict__ for course in courses],
        'faculties': [faculty.__dict__ for faculty in faculties],
        'classrooms': [classroom.__dict__ for classroom in classrooms],
        'sections': [section.__dict__ for section in sections],
        'time_slots': [time_slot.__dict__ for time_slot in time_slots],
        'message': 'Data loaded (no filtering yet)'
    }
    return JsonResponse(timetable_data)