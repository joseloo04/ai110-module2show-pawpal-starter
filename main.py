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
    dog.add_task(Task(name="Morning Walk", duration_minutes=30, priority="HIGH"))
    dog.add_task(Task(name="Feeding", duration_minutes=10, priority="HIGH"))
    dog.add_task(Task(name="Playtime", duration_minutes=20, priority="MEDIUM"))

    # Add tasks to cat (Whiskers)
    cat.add_task(Task(name="Litter Box Cleaning", duration_minutes=15, priority="HIGH"))
    cat.add_task(Task(name="Feeding", duration_minutes=5, priority="HIGH"))
    cat.add_task(Task(name="Grooming", duration_minutes=25, priority="MEDIUM"))

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


if __name__ == "__main__":
    main()
