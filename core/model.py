from dataclasses import dataclass, field
from typing import List, Optional 

@dataclass
class TimeSlot:
    day: str  # e.g., "Monday", "Tuesday"
    start_time: str  # e.g., "09:00", "10:30"
    end_time: str    # e.g., "10:00", "11:30"

@dataclass
class Course:
    course_code: str
    name: str
    credits: int
    department: str
    lecture_hours: int
    lab_hours: int
    required_features: List[str] = field(default_factory=list)
    is_core: bool = False

@dataclass
class Faculty:
    faculty_id: str
    name: str
    department: str
    availability: List[TimeSlot] = field(default_factory=list)

@dataclass
class Classroom:
    room_id: str
    capacity: int
    location: Optional[str] = None
    features: List[str] = field(default_factory=list)

@dataclass
class Section:
    section_id: str
    course_code: str
    capacity: int

@dataclass
class ScheduledClass:
    course: Course
    section: Section
    faculty: Faculty
    classroom: Classroom
    time_slot: TimeSlot