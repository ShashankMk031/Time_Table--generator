from typing import List

from core.model import Classroom
from .model import ScheduledClass, TimeSlot, Course, Section

# --- Hard Constraints ---

def check_faculty_conflict(schedule: List[ScheduledClass], new_class: ScheduledClass) -> bool:
    for scheduled in schedule:
        if scheduled.faculty == new_class.faculty and scheduled.time_slot == new_class.time_slot:
            return True
    return False

def check_classroom_conflict(schedule: List[ScheduledClass], new_class: ScheduledClass) -> bool:
    for scheduled in schedule:
        if scheduled.classroom == new_class.classroom and scheduled.time_slot == new_class.time_slot:
            return True
    return False

def check_room_capacity(new_class: ScheduledClass) -> bool:
    return new_class.classroom.capacity >= new_class.section.capacity

def check_course_section_overlap(schedule: List[ScheduledClass], new_class: ScheduledClass) -> bool:
    for scheduled in schedule:
        if scheduled.section == new_class.section and scheduled.time_slot == new_class.time_slot:
            return True
    return False

def check_faculty_availability(new_class: ScheduledClass) -> bool:
    for available_slot in new_class.faculty.availability:
        if available_slot.day == new_class.time_slot.day and \
           available_slot.start_time <= new_class.time_slot.start_time and \
           available_slot.end_time >= new_class.time_slot.end_time:
            return True
    return False

def check_room_requirements(new_class: ScheduledClass) -> bool:
    if hasattr(new_class.course, 'required_features') and new_class.course.required_features:
        for feature in new_class.course.required_features:
            if feature not in new_class.classroom.features:
                return False
    return True

# --- Soft Constraints (Placeholders for now) ---
# We will implement these later based on your specific soft constraints
def score_faculty_preference(new_class: ScheduledClass) -> int: return 0
def score_minimize_student_gaps(schedule: List[ScheduledClass], new_class: ScheduledClass, all_sections: List[Section]) -> int: return 0
def score_prefer_morning_core_courses(new_class: ScheduledClass) -> int: return 0
def score_balance_faculty_workload(schedule: List[ScheduledClass], new_class: ScheduledClass) -> int: return 0
def score_optimize_room_utilization(schedule: List[ScheduledClass], all_classrooms: List[Classroom]) -> int: return 0