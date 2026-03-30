from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from datetime import datetime, timedelta


@dataclass
class Owner:
    """Represents a pet owner who manages pets and their care tasks."""
    name: str
    available_minutes_per_day: int
    pets: List['Pet'] = field(default_factory=list)

    # Add a pet to the owner's list
    def add_pet(self, pet: 'Pet') -> None:
        self.pets.append(pet)

    # Remove a pet by name from the owner's list
    def remove_pet(self, pet_name: str) -> bool:
        for i, pet in enumerate(self.pets):
            if pet.name == pet_name:
                self.pets.pop(i)
                return True
        return False

    # Get all tasks across all pets
    def get_all_tasks(self) -> List['Task']:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Pet:
    """Represents a pet that belongs to an owner and has associated care tasks."""
    name: str
    species: str
    age_years: float
    tasks: List['Task'] = field(default_factory=list)

    # Add a task to the pet's list
    def add_task(self, task: 'Task') -> None:
        self.tasks.append(task)

    # Remove a task by name from the pet's list
    def remove_task(self, task_name: str) -> bool:
        for i, task in enumerate(self.tasks):
            if task.name == task_name:
                self.tasks.pop(i)
                return True
        return False

@dataclass
class Task:
    """Represents a single care activity for a pet, with duration and priority."""
    name: str
    duration_minutes: int
    priority: str
    completed: bool = field(default=False)  # completed field
    scheduled_time: str = "00:00"
    recurrence: str = "none"

    # Return the priority level of the task
    def get_priority_level(self) -> str:
        return self.priority.lower()

    def mark_complete(self, pet: Optional['Pet'] = None) -> Optional['Task']:
        """Mark task complete and auto-generate next occurrence if recurring."""
        self.completed = True
        if pet and self.recurrence in ("daily", "weekly"):
            new_task = Task(
                name=self.name,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                scheduled_time=self.scheduled_time,
                recurrence=self.recurrence,
                completed=False
            )
            pet.add_task(new_task)
            return new_task
        return None


class Scheduler:
    """Handles the logic for scheduling pet care tasks based on owner constraints and priorities."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks = owner.get_all_tasks()

    # Generate a daily plan of tasks
    def generate_daily_plan(self) -> List[Task]:
        included, _ = self.fit_tasks_into_time()
        return included

    # Sort tasks by priority
    def sort_tasks_by_priority(self) -> List[Task]:
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(
            self.tasks,
            key=lambda task: priority_order.get(task.get_priority_level(), 3)
        )

    # Filter tasks by a specific priority level
    def filter_tasks_by_priority(self, level: str) -> List[Task]:
        normalized_level = level.lower()
        return [task for task in self.tasks if task.get_priority_level() == normalized_level]

    def sort_tasks_by_time(self) -> List[Task]:
        """Sort all tasks by scheduled time in HH:MM format."""
        def time_to_int(time_str: str) -> int:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 100 + minutes
        return sorted(self.tasks, key=lambda task: time_to_int(task.scheduled_time))

    def detect_time_conflicts(self) -> Dict[str, List[Task]]:
        """Return tasks grouped by scheduled time, including only times with multiple tasks."""
        time_groups: Dict[str, List[Task]] = {}
        for task in self.tasks:
            if task.scheduled_time not in time_groups:
                time_groups[task.scheduled_time] = []
            time_groups[task.scheduled_time].append(task)
        return {time: tasks for time, tasks in time_groups.items() if len(tasks) > 1}

    def filter_tasks_by_completion(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.tasks if task.completed == completed]

    def filter_tasks_by_pet_name(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to a specific pet."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.tasks
        return []

    # Fit tasks into available time, returning included and excluded tasks
    def fit_tasks_into_time(self, max_minutes: int = None) -> Tuple[List[Task], List[Task]]:
        if max_minutes is None:
            max_minutes = self.owner.available_minutes_per_day

        sorted_tasks = self.sort_tasks_by_priority()
        included = []
        excluded = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= max_minutes:
                included.append(task)
                time_used += task.duration_minutes
            else:
                excluded.append(task)

        return (included, excluded)

    # Provide an explanation for the given plan
    def explain_plan(self, plan: List[Task]) -> str:
        if not plan:
            return "No tasks scheduled."

        lines = ["Scheduled tasks:"]
        total_time = 0

        for task in plan:
            lines.append(f"  - {task.name}: {task.duration_minutes} minutes")
            total_time += task.duration_minutes

        lines.append(f"\nTotal time: {total_time} minutes")

        return "\n".join(lines)
