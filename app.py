import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=120)

st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name, key="owner_name_input")
available_minutes = st.number_input(
    "Available minutes per day",
    min_value=15,
    max_value=1440,
    value=st.session_state.owner.available_minutes_per_day,
    key="available_minutes_input"
)

# Update owner if inputs changed (preserve existing pets)
if owner_name != st.session_state.owner.name or available_minutes != st.session_state.owner.available_minutes_per_day:
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_minutes_per_day = available_minutes

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age_years=1.0)
    st.session_state.owner.add_pet(new_pet)
    st.rerun()

# Display current pets
if st.session_state.owner.pets:
    st.write("**Your Pets:**")
    pet_data = [
        {"Name": pet.name, "Species": pet.species, "Age (years)": pet.age_years, "Tasks": len(pet.tasks)}
        for pet in st.session_state.owner.pets
    ]
    st.table(pet_data)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to your pet. These will feed into your scheduler.")

# Let user select which pet to add tasks to
if st.session_state.owner.pets:
    selected_pet_name = st.selectbox(
        "Select pet to add tasks to",
        [pet.name for pet in st.session_state.owner.pets]
    )
    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        task = Task(name=task_title, duration_minutes=int(duration), priority=priority)
        selected_pet.add_task(task)
        st.rerun()

    if selected_pet.tasks:
        st.write(f"Tasks for {selected_pet.name}:")
        task_data = [
            {"Task": task.name, "Duration (min)": task.duration_minutes, "Priority": task.priority}
            for task in selected_pet.tasks
        ]
        st.table(task_data)
    else:
        st.info(f"No tasks yet for {selected_pet.name}. Add one above.")
else:
    st.warning("Add a pet first to create tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    daily_plan = scheduler.generate_daily_plan()

    st.subheader("📅 Your Daily Schedule")

    if daily_plan:
        # Display plan as table
        plan_data = [
            {"Task": task.name, "Duration (min)": task.duration_minutes, "Priority": task.priority}
            for task in daily_plan
        ]
        st.table(plan_data)

        # Display summary
        total_scheduled = sum(task.duration_minutes for task in daily_plan)
        remaining = st.session_state.owner.available_minutes_per_day - total_scheduled

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Scheduled", f"{total_scheduled} min")
        with col2:
            st.metric("Available Time", f"{st.session_state.owner.available_minutes_per_day} min")
        with col3:
            st.metric("Remaining", f"{remaining} min")
        
        #Show excluded tasks
        included, excluded = scheduler.fit_tasks_into_time()
        if excluded:
            st.warning(f"{len(excluded)} task(s) could not fit in your available time:")
            for task in excluded:
                st.write(f"- {task.name} ({task.duration_minutes} min, {task.priority} priority)")
    else:
        st.warning("No tasks fit within the available time.")
