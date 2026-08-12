import streamlit as st
import pandas as pd

from predictor import (
    predict_category,
    predict_priority,
    recommend_assignee,
    status_mapping
)

from database import (
    create_database,
    save_task,
    get_tasks,
    get_statistics
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

create_database()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="AI Task Management System",

    page_icon="🤖",

    layout="wide"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🤖 AI Task Manager"
)

page = st.sidebar.radio(

    "Navigation",

    [
        "🏠 Task Analyzer",
        "📊 Dashboard",
        "📋 Task History"
    ]
)


# ============================================================
# TASK ANALYZER
# ============================================================

if page == "🏠 Task Analyzer":

    st.title(
        "🤖 AI-Powered Task Management System"
    )

    st.write(
        "Automatically classify tasks, predict priority "
        "and recommend the best team member."
    )

    st.divider()

    st.header(
        "📝 Create New Task"
    )


    # --------------------------------------------------------
    # TASK DESCRIPTION
    # --------------------------------------------------------

    task_description = st.text_area(

        "Task Description",

        placeholder=(
            "Example: Fix database security vulnerability"
        ),

        height=120
    )


    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        estimated_hours = st.number_input(

            "Estimated Hours",

            min_value=1.0,

            max_value=1000.0,

            value=5.0,

            step=1.0
        )


    with col2:

        completed_hours = st.number_input(

            "Completed Hours",

            min_value=0.0,

            max_value=1000.0,

            value=0.0,

            step=1.0
        )


    col3, col4 = st.columns(2)


    with col3:

        days_to_deadline = st.number_input(

            "Days To Deadline",

            min_value=0,

            max_value=365,

            value=7,

            step=1
        )


    with col4:

        status_options = []

        for key, value in status_mapping.items():

            if isinstance(key, str):

                status_options.append(key)

            elif isinstance(value, str):

                status_options.append(value)


        status_options = list(
            dict.fromkeys(status_options)
        )


        if not status_options:

            status_options = [
                "Pending",
                "In Progress",
                "Completed"
            ]


        status = st.selectbox(

            "Task Status",

            status_options
        )


    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    st.divider()


    if st.button(

        "🚀 Analyze Task",

        use_container_width=True,

        type="primary"

    ):

        if not task_description.strip():

            st.warning(
                "Please enter a task description."
            )

            st.stop()


        # ----------------------------------------------------
        # REMAINING HOURS
        # ----------------------------------------------------

        remaining_hours = (

            estimated_hours
            -
            completed_hours

        )

        if remaining_hours < 0:

            remaining_hours = 0


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        with st.spinner(
            "Analyzing task category..."
        ):

            category = predict_category(
                task_description
            )


        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        with st.spinner(
            "Predicting task priority..."
        ):

            priority = predict_priority(

                estimated_hours,

                completed_hours,

                status,

                remaining_hours,

                days_to_deadline,

                category
            )


        # ----------------------------------------------------
        # ASSIGNEE
        # ----------------------------------------------------

        with st.spinner(
            "Finding the best team member..."
        ):

            assignee = recommend_assignee(

                estimated_hours
            )


        # ----------------------------------------------------
        # SAVE TASK
        # ----------------------------------------------------

        save_task(

            task_description,

            category,

            priority,

            estimated_hours,

            completed_hours,

            remaining_hours,

            days_to_deadline,

            status,

            assignee
        )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            "✅ Task analyzed and saved successfully!"
        )


        st.divider()


        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        st.header(
            "📊 AI Analysis Results"
        )


        result1, result2, result3 = st.columns(3)


        with result1:

            st.subheader(
                "📂 Category"
            )

            st.info(
                str(category)
            )


        with result2:

            st.subheader(
                "⚡ Priority"
            )

            if str(priority).lower() == "critical":

                st.error(
                    str(priority)
                )

            elif str(priority).lower() == "high":

                st.warning(
                    str(priority)
                )

            else:

                st.success(
                    str(priority)
                )


        with result3:

            st.subheader(
                "👤 Recommended Assignee"
            )

            st.success(
                str(assignee)
            )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        st.divider()

        st.header(
            "📋 Task Summary"
        )


        summary1, summary2 = st.columns(2)


        with summary1:

            st.write(
                f"**Task:** {task_description}"
            )

            st.write(
                f"**Category:** {category}"
            )

            st.write(
                f"**Priority:** {priority}"
            )


        with summary2:

            st.write(
                f"**Estimated Hours:** {estimated_hours}"
            )

            st.write(
                f"**Completed Hours:** {completed_hours}"
            )

            st.write(
                f"**Remaining Hours:** {remaining_hours}"
            )

            st.write(
                f"**Days To Deadline:** {days_to_deadline}"
            )

            st.write(
                f"**Status:** {status}"
            )

            st.write(
                f"**Assigned To:** {assignee}"
            )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.title(
        "📊 Task Management Dashboard"
    )

    st.write(
        "Overview of analyzed tasks and team workload."
    )


    (
        total_tasks,
        priority_data,
        category_data,
        assignee_data
    ) = get_statistics()


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Tasks",
            int(total_tasks)
        )


    with col2:

        high_count = 0

        for _, row in priority_data.iterrows():

            if str(row["priority"]).lower() in [
                "high",
                "critical"
            ]:

                high_count += int(
                    row["count"]
                )

        st.metric(
            "High/Critical",
            high_count
        )


    with col3:

        categories = len(
            category_data
        )

        st.metric(
            "Categories",
            categories
        )


    with col4:

        team_members = len(
            assignee_data
        )

        st.metric(
            "Team Members",
            team_members
        )


    st.divider()


    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    chart1, chart2 = st.columns(2)


    with chart1:

        st.subheader(
            "⚡ Priority Distribution"
        )

        if not priority_data.empty:

            st.bar_chart(
                priority_data.set_index(
                    "priority"
                )
            )

        else:

            st.info(
                "No task data available yet."
            )


    with chart2:

        st.subheader(
            "📂 Category Distribution"
        )

        if not category_data.empty:

            st.bar_chart(
                category_data.set_index(
                    "category"
                )
            )

        else:

            st.info(
                "No task data available yet."
            )


    st.divider()


    st.subheader(
        "👥 Tasks Assigned to Team Members"
    )


    if not assignee_data.empty:

        st.bar_chart(

            assignee_data.set_index(
                "assigned_to"
            )
        )

    else:

        st.info(
            "No assignment data available yet."
        )


# ============================================================
# TASK HISTORY
# ============================================================

elif page == "📋 Task History":

    st.title(
        "📋 Task History"
    )

    st.write(
        "Previously analyzed tasks."
    )


    tasks = get_tasks()


    if tasks.empty:

        st.info(
            "No tasks have been analyzed yet."
        )

    else:

        # Remove database ID for display

        display_tasks = tasks.drop(
            columns=["id"],
            errors="ignore"
        )


        st.dataframe(

            display_tasks,

            use_container_width=True,

            hide_index=True
        )


        st.divider()


        st.subheader(
            "🔎 Filter Tasks"
        )


        # ----------------------------------------------------
        # PRIORITY FILTER
        # ----------------------------------------------------

        priorities = [

            "All"
        ] + sorted(

            display_tasks[
                "priority"
            ].dropna().unique().tolist()
        )


        selected_priority = st.selectbox(

            "Priority",

            priorities
        )


        filtered_tasks = display_tasks.copy()


        if selected_priority != "All":

            filtered_tasks = filtered_tasks[
                filtered_tasks[
                    "priority"
                ] == selected_priority
            ]


        st.dataframe(

            filtered_tasks,

            use_container_width=True,

            hide_index=True
        )