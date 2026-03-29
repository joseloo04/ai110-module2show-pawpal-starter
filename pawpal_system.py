from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Owner:
    """Represents a pet owner who manages pets and their care tasks."""
    name: str
    available_minutes_per_day: int
    pets: List['Pet'] = field(default_factory=list)

    # Add a pet to the owner's list
    def add_pet(self, pet: 'Pet') -> None:
        pass

    # Remove a pet by name from the owner's list
    def remove_pet(self, pet_name: str) -> bool:
        pass


@dataclass
class Pet:
    """Represents a pet that belongs to an owner and has associated care tasks."""
    name: str
    species: str
    age_years: float
    tasks: List['Task'] = field(default_factory=list)

    # Add a task to the pet's list
    def add_task(self, task: 'Task') -> None:
        pass

    # Remove a task by name from the pet's list
    def remove_task(self, task_name: str) -> bool:
        pass


@dataclass
class Task:
    """Represents a single care activity for a pet, with duration and priority."""
    name: str
    duration_minutes: int
    priority: str

    # Return the priority level of the task
    def get_priority_level(self) -> str:
        pass


class Scheduler:
    """Handles the logic for scheduling pet care tasks based on owner constraints and priorities."""

    def __init__(self, owner: Owner, tasks: List[Task]):
        self.owner = owner
        self.tasks = tasks

    # Generate a daily plan of tasks
    def generate_daily_plan(self) -> List[Task]:
        pass

    # Sort tasks by priority
    def sort_tasks_by_priority(self) -> List[Task]:
        pass

    # Filter tasks by a specific priority level
    def filter_tasks_by_priority(self, level: str) -> List[Task]:
        pass

    # Fit tasks into available time, returning included and excluded tasks
    def fit_tasks_into_time(self, max_minutes: int = None) -> Tuple[List[Task], List[Task]]:
        pass

    # Provide an explanation for the given plan
    def explain_plan(self, plan: List[Task]) -> str:
        pass
