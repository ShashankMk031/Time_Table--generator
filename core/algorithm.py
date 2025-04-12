import random
from typing import List, Callable
from .model import Course, Faculty, Classroom, Section, TimeSlot, ScheduledClass
from .constraints import (
    check_faculty_conflict,
    check_classroom_conflict,
    check_room_capacity,
    check_course_section_overlap,
    check_faculty_availability,
    check_room_requirements,
)
from .utils import load_courses, load_faculties, load_classrooms, load_sections, load_time_slots

# --- GA Parameters (will need tuning) ---
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8

# --- Chromosome Representation ---
# A chromosome will be a list of ScheduledClass objects representing a potential timetable.

def create_individual(
    courses: List[Course],
    faculties: List[Faculty],
    classrooms: List[Classroom],
    sections: List[Section],
    time_slots: List[TimeSlot]
) -> List[ScheduledClass]:
    individual: List[ScheduledClass] = []
    for course in courses:
        for section in [s for s in sections if s.course_code == course.course_code]:
            faculty = random.choice([f for f in faculties if f.department == course.department])
            classroom = random.choice(classrooms)
            time_slot = random.choice(time_slots)
            individual.append(ScheduledClass(course, section, faculty, classroom, time_slot))
    return individual

def calculate_fitness(individual: List[ScheduledClass], hard_constraints: List[Callable[[List[ScheduledClass], ScheduledClass], bool]], soft_constraints: List[Callable[[List[ScheduledClass], ScheduledClass], int]]) -> float:
    hard_violations = 0
    soft_score = 0
    for i, scheduled_class in enumerate(individual):
        for constraint in hard_constraints:
            if constraint == check_faculty_conflict or constraint == check_classroom_conflict or constraint == check_course_section_overlap:
                if constraint(individual[:i] + individual[i+1:], scheduled_class):
                    hard_violations += 1
            elif constraint(scheduled_class) is False:  # For single-class constraints
                hard_violations += 1
        for soft_constraint in soft_constraints:
            soft_score += soft_constraint(individual, scheduled_class)
    fitness = -hard_violations + (soft_score / len(individual) if individual else 0)
    return fitness

def selection(population: List[List[ScheduledClass]], fitness_scores: List[float], num_parents: int) -> List[List[ScheduledClass]]:
    return random.sample(population, num_parents) # Placeholder

def crossover(parents: List[List[ScheduledClass]]) -> List[List[ScheduledClass]]:
    offspring: List[List[ScheduledClass]] = []
    for i in range(0, len(parents), 2):
        if i + 1 < len(parents) and random.random() < CROSSOVER_RATE:
            parent1 = parents[i]
            parent2 = parents[i+1]
            crossover_point = random.randint(0, len(parent1))
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[:crossover_point]
            offspring.extend([child1, child2])
        else:
            offspring.append(parents[i])
    return offspring

def mutate(individual: List[ScheduledClass], courses: List[Course], faculties: List[Faculty], classrooms: List[Classroom], time_slots: List[TimeSlot]) -> List[ScheduledClass]:
    mutated_individual = list(individual)
    if random.random() < MUTATION_RATE:
        index_to_mutate = random.randint(0, len(mutated_individual) - 1)
        attribute_to_change = random.choice(['faculty', 'classroom', 'time_slot'])
        if attribute_to_change == 'faculty':
            mutated_individual[index_to_mutate].faculty = random.choice([f for f in faculties if f.department == mutated_individual[index_to_mutate].course.department])
        elif attribute_to_change == 'classroom':
            mutated_individual[index_to_mutate].classroom = random.choice(classrooms)
        elif attribute_to_change == 'time_slot':
            mutated_individual[index_to_mutate].time_slot = random.choice(time_slots)
    return mutated_individual

def evolve_timetable(
    courses: List[Course],
    faculties: List[Faculty],
    classrooms: List[Classroom],
    sections: List[Section],
    time_slots: List[TimeSlot],
    hard_constraints: List[Callable[[List[ScheduledClass], ScheduledClass], bool]],
    soft_constraints: List[Callable[[List[ScheduledClass], ScheduledClass], int]]
) -> List[ScheduledClass]:
    population = [create_individual(courses, faculties, classrooms, sections, time_slots) for _ in range(POPULATION_SIZE)]
    for generation in range(GENERATIONS):
        fitness_scores = [calculate_fitness(individual, hard_constraints, soft_constraints) for individual in population]
        parents = selection(population, fitness_scores, POPULATION_SIZE // 2)
        offspring = crossover(parents)
        mutated_offspring = [mutate(child, courses, faculties, classrooms, time_slots) for child in offspring]
        population = parents + mutated_offspring
        best_fitness = max(fitness_scores)
        print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")
    best_individual = population[fitness_scores.index(max(fitness_scores))]
    return best_individual

hard_constraints_list: List[Callable[[List[ScheduledClass], ScheduledClass], bool]] = [
    check_faculty_conflict,
    check_classroom_conflict,
    check_room_capacity,
    check_course_section_overlap,
    check_faculty_availability,
    check_room_requirements,
]

soft_constraints_list: List[Callable[[List[ScheduledClass], ScheduledClass], int]] = []

if __name__ == "__main__":
    data_dir = "data/"
    courses_data = load_courses(data_dir + "courses.json")
    faculties_data = load_faculties(data_dir + "faculties.json")
    classrooms_data = load_classrooms(data_dir + "classrooms.json")
    sections_data = load_sections(data_dir + "sections.json")
    time_slots_data = load_time_slots(data_dir + "time_slots.json")

    best_timetable = evolve_timetable(
        courses_data,
        faculties_data,
        classrooms_data,
        sections_data,
        time_slots_data,
        hard_constraints_list,
        soft_constraints_list
    )

    print("\n--- Best Timetable Found ---")
    for scheduled_class in best_timetable:
        print(f"{scheduled_class.course.name} (Sec: {scheduled_class.section.section_id}) with {scheduled_class.faculty.name} in {scheduled_class.classroom.room_id} at {scheduled_class.time_slot.day} {scheduled_class.time_slot.start_time}-{scheduled_class.time_slot.end_time}")