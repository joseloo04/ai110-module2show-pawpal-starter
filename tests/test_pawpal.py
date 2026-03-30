from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() changes the task's completed status."""
    task = Task(name="Walk", duration_minutes=30, priority="HIGH")
    assert task.completed == False

    task.mark_complete()

    assert task.completed == True


def test_add_task_increases_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Max", species="Dog", age_years=3)
    initial_count = len(pet.tasks)
    assert initial_count == 0

    task = Task(name="Walk", duration_minutes=30, priority="HIGH")
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
