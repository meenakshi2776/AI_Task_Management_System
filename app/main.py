import streamlit as st

from predictor import (
    predict_category,
    predict_priority,
    recommend_assignee,
    status_mapping
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="AI Task Management System",

    page_icon="🤖",

    layout="wide"
)


# ============================================================
# CUSTOM TITLE
# ============================================================

st.title(
    "🤖 AI-Powered Task Management System"
)

st.write(
    "Automatically classify tasks, predict priority "
    "and recommend the best team member."
)


st.divider()


# ============================================================
# CREATE TASK SECTION
# ============================================================

st.header(
    "📝 Create New Task"
)


# ============================================================
# TASK DESCRIPTION
# ============================================================

task_description = st.text_area(

    "Task Description",

    placeholder=(
        "Example: Fix database security vulnerability"
    ),

    height=120
)


# ============================================================
# INPUT COLUMNS
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# ESTIMATED HOURS
# ============================================================

with col1:

    estimated_hours = st.number_input(

        "Estimated Hours",

        min_value=1.0,

        max_value=1000.0,

        value=5.0,

        step=1.0
    )


# ============================================================
# COMPLETED HOURS
# ============================================================

with col2:

    completed_hours = st.number_input(

        "Completed Hours",

        min_value=0.0,

        max_value=1000.0,

        value=0.0,

        step=1.0
    )


# ============================================================
# SECOND ROW
# ============================================================

col3, col4 = st.columns(2)


# ============================================================
# DAYS TO DEADLINE
# ============================================================

with col3:

    days_to_deadline = st.number_input(

        "Days To Deadline",

        min_value=0,

        max_value=365,

        value=7,

        step=1
    )


# ============================================================
# STATUS
# ============================================================

with col4:

    # Extract status names from mapping

    status_options = []

    for key, value in status_mapping.items():

        if isinstance(key, str):

            status_options.append(key)

        elif isinstance(value, str):

            status_options.append(value)


    # Remove duplicates

    status_options = list(
        dict.fromkeys(status_options)
    )


    # Fallback if mapping format is unexpected

    if not status_options:

        status_options = [
            "Not Started",
            "In Progress",
            "Completed"
        ]


    status = st.selectbox(

        "Task Status",

        status_options
    )


# ============================================================
# ANALYZE TASK BUTTON
# ============================================================

st.divider()


analyze_button = st.button(

    "🚀 Analyze Task",

    use_container_width=True,

    type="primary"
)


# ============================================================
# ANALYZE TASK
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # Validate task description
    # --------------------------------------------------------

    if not task_description.strip():

        st.warning(
            "⚠️ Please enter a task description."
        )

        st.stop()


    # --------------------------------------------------------
    # Calculate remaining hours
    # --------------------------------------------------------

    remaining_hours = (

        estimated_hours

        -

        completed_hours

    )


    # Prevent negative remaining hours

    if remaining_hours < 0:

        remaining_hours = 0


    # --------------------------------------------------------
    # STEP 1: CATEGORY PREDICTION
    # --------------------------------------------------------

    with st.spinner(
        "Analyzing task category..."
    ):

        category = predict_category(
            task_description
        )


    # --------------------------------------------------------
    # STEP 2: PRIORITY PREDICTION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # STEP 3: WORKLOAD BALANCING
    # --------------------------------------------------------

    with st.spinner(
        "Finding the best team member..."
    ):

        assignee = recommend_assignee(

            estimated_hours

        )


    # ========================================================
    # RESULTS
    # ========================================================

    st.success(
        "✅ Task analyzed successfully!"
    )


    st.divider()


    st.header(
        "📊 AI Analysis Results"
    )


    # --------------------------------------------------------
    # RESULT COLUMNS
    # --------------------------------------------------------

    result1, result2, result3 = st.columns(3)


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    with result1:

        st.subheader(
            "📂 Category"
        )

        st.info(
            str(category)
        )


    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    with result2:

        st.subheader(
            "⚡ Priority"
        )

        priority_text = str(
            priority
        )

        if priority_text.lower() == "critical":

            st.error(
                priority_text
            )

        elif priority_text.lower() == "high":

            st.warning(
                priority_text
            )

        else:

            st.success(
                priority_text
            )


    # --------------------------------------------------------
    # ASSIGNEE
    # --------------------------------------------------------

    with result3:

        st.subheader(
            "👤 Recommended Assignee"
        )

        st.success(
            str(assignee)
        )


    # ========================================================
    # TASK SUMMARY
    # ========================================================

    st.divider()


    st.header(
        "📋 Task Summary"
    )


    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        st.write(
            "**Task Description:**"
        )

        st.write(
            task_description
        )

        st.write(
            f"**Category:** {category}"
        )

        st.write(
            f"**Priority:** {priority}"
        )


    with summary_col2:

        st.write(
            f"**Estimated Hours:** "
            f"{estimated_hours}"
        )

        st.write(
            f"**Completed Hours:** "
            f"{completed_hours}"
        )

        st.write(
            f"**Remaining Hours:** "
            f"{remaining_hours}"
        )

        st.write(
            f"**Days To Deadline:** "
            f"{days_to_deadline}"
        )

        st.write(
            f"**Status:** "
            f"{status}"
        )

        st.write(
            f"**Recommended Assignee:** "
            f"{assignee}"
        )


    # ========================================================
    # SYSTEM FLOW
    # ========================================================

    st.divider()


    st.header(
        "🔄 AI Decision Pipeline"
    )


    st.write(
        f"""
        **Task Description**
        ↓
        **TF-IDF + Classifier**
        ↓
        **Category: {category}**
        ↓
        **Priority Prediction Model**
        ↓
        **Priority: {priority}**
        ↓
        **Workload Balancer**
        ↓
        **Recommended Assignee: {assignee}**
        """
    )