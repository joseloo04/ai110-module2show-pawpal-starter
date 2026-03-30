from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an owner
    owner = Owner(name="Alex", available_minutes_per_day=120)

    # Create pets and add to owner
    dog = Pet(name="Max", species="Golden Retriever", age_years=3)
    cat = Pet(name="Whiskers", species="Tabby Cat", age_years=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks to dog (Max)
    dog.add_task(Task(name="Morning Walk", duration_minutes=30, priority="HIGH", scheduled_time="08:00", recurrence="daily"))
    dog.add_task(Task(name="Feeding", duration_minutes=10, priority="HIGH", scheduled_time="08:30", recurrence="none"))
    dog.add_task(Task(name="Playtime", duration_minutes=20, priority="MEDIUM", scheduled_time="10:00", recurrence="none"))

    # Add tasks to cat (Whiskers)
    cat.add_task(Task(name="Litter Box Cleaning", duration_minutes=15, priority="HIGH", scheduled_time="08:30", recurrence="none"))
    cat.add_task(Task(name="Feeding", duration_minutes=5, priority="HIGH", scheduled_time="08:30", recurrence="none"))
    cat.add_task(Task(name="Grooming", duration_minutes=25, priority="MEDIUM", scheduled_time="14:00", recurrence="none"))

    # Create scheduler with the owner
    scheduler = Scheduler(owner)

    # Generate and display today's schedule
    included, excluded = scheduler.fit_tasks_into_time()
    daily_plan = included

    print("=" * 50)
    print(f"TODAY'S SCHEDULE FOR {owner.name.upper()}")
    print("=" * 50)
    print(f"Available time: {owner.available_minutes_per_day} minutes")
    print()

    # Display which pet each task belongs to
    print("Tasks by Pet:")
    for pet in owner.pets:
        print(f"\n📍 {pet.name} ({pet.species}, {pet.age_years} years old)")
        for task in pet.tasks:
            status = "✓" if task.completed else "○"
            print(f"   {status} {task.name}: {task.duration_minutes} min [{task.priority}]")

    print()
    print("=" * 50)
    print("SCHEDULED PLAN:")
    print("=" * 50)

    # Display the scheduled plan with explanation
    if daily_plan:
        for i, task in enumerate(daily_plan, 1):
            # Find which pet this task belongs to
            pet_name = None
            for pet in owner.pets:
                if task in pet.tasks:
                    pet_name = pet.name
                    break
            pet_info = f" - {pet_name}" if pet_name else ""
            print(f"{i}. {task.name}{pet_info} ({task.duration_minutes} min)")
        total_scheduled = sum(task.duration_minutes for task in daily_plan)
        print(f"\n✓ Total Time Scheduled: {total_scheduled} minutes")
        print(f"  Remaining Available: {owner.available_minutes_per_day - total_scheduled} minutes")
    else:
        print("No tasks could fit in the available time.")

    # Show what couldn't fit
    if excluded:
        print(f"\n⚠ Could not fit ({len(excluded)} tasks):")
        for task in excluded:
            # Find which pet this task belongs to
            pet_name = None
            for pet in owner.pets:
                if task in pet.tasks:
                    pet_name = pet.name
                    break
            pet_info = f" - {pet_name}" if pet_name else ""
            print(f"   - {task.name}{pet_info} ({task.duration_minutes} min)")

    print("\n" + "=" * 50)

    # Feature 1: Sorting by time
    print("\n" + "=" * 50)
    print("FEATURE 1: SORTING BY TIME")
    print("=" * 50)
    sorted_by_time = scheduler.sort_tasks_by_time()
    if sorted_by_time:
        for task in sorted_by_time:
            print(f"  {task.scheduled_time} - {task.name}")
    else:
        print("  No tasks to sort")

    # Feature 2: Conflict detection
    print("\n" + "=" * 50)
    print("FEATURE 2: CONFLICT DETECTION")
    print("=" * 50)
    conflicts = scheduler.detect_time_conflicts()
    if conflicts:
        for time_slot, conflicting_tasks in sorted(conflicts.items()):
            print(f"\n⚠ WARNING: Time slot {time_slot} has {len(conflicting_tasks)} overlapping tasks:")
            for task in conflicting_tasks:
                print(f"     - {task.name}")
    else:
        print("  No time conflicts detected")

    # Feature 3: Filtering by completion
    print("\n" + "=" * 50)
    print("FEATURE 3: FILTERING BY COMPLETION")
    print("=" * 50)
    # Mark one task as complete (Litter Box Cleaning)
    litter_task = cat.tasks[0]  # Litter Box Cleaning is the first task added to cat
    print(f"Marking task complete: {litter_task.name}")
    litter_task.mark_complete()

    incomplete_tasks = scheduler.filter_tasks_by_completion(False)
    print(f"\nIncomplete tasks ({len(incomplete_tasks)} remaining):")
    for task in incomplete_tasks:
        print(f"  - {task.name} ({task.priority})")

    # Feature 4: Recurring tasks
    print("\n" + "=" * 50)
    print("FEATURE 4: RECURRING TASKS")
    print("=" * 50)
    morning_walk = dog.tasks[0]  # Morning Walk is the first task added to dog
    print(f"Completing daily recurring task: {morning_walk.name}")
    new_task = morning_walk.mark_complete(pet=dog)

    if new_task:
        print(f"✓ New occurrence created automatically!")
        print(f"  Original task: {morning_walk.name} [completed: {morning_walk.completed}]")
        print(f"  New task: {new_task.name} [completed: {new_task.completed}]")

    print(f"\n{dog.name}'s updated task list ({len(dog.tasks)} total):")
    for i, task in enumerate(dog.tasks, 1):
        status = "✓ completed" if task.completed else "○ incomplete"
        print(f"  {i}. {task.name} - {status} [recurrence: {task.recurrence}]")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
