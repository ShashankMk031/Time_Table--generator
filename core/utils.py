import json
from typing import List
from .model import Course, Faculty, Classroom, Section, TimeSlot

def load_courses(file_path: str) -> List[Course]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [Course(**item) for item in data]

def load_faculties(file_path: str) -> List[Faculty]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    faculties = []
    for item in data:
        item['availability'] = [TimeSlot(**avail) for avail in item.get('availability', [])]
        faculties.append(Faculty(**item))
    return faculties

def load_classrooms(file_path: str) -> List[Classroom]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [Classroom(**item) for item in data]

def load_sections(file_path: str) -> List[Section]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [Section(**item) for item in data]

def load_time_slots(file_path: str) -> List[TimeSlot]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [TimeSlot(**item) for item in data]