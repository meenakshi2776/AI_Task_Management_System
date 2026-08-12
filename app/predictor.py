import os
import joblib
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "task_dataset_cleaned.csv"
)


# ============================================================
# LOAD TRAINED MODELS
# ============================================================

classifier = joblib.load(
    os.path.join(
        MODEL_DIR,
        "task_classifier.pkl"
    )
)

tfidf = joblib.load(
    os.path.join(
        MODEL_DIR,
        "tfidf_vectorizer.pkl"
    )
)

priority_model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "priority_predictor.pkl"
    )
)

priority_features = joblib.load(
    os.path.join(
        MODEL_DIR,
        "priority_features.pkl"
    )
)

category_mapping = joblib.load(
    os.path.join(
        MODEL_DIR,
        "category_mapping.pkl"
    )
)

status_mapping = joblib.load(
    os.path.join(
        MODEL_DIR,
        "status_mapping.pkl"
    )
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_code_from_mapping(value, mapping):
    """
    Convert a category/status name into its numerical code.

    Handles both possible mapping formats:

    {
        "Security": 5
    }

    or

    {
        5: "Security"
    }
    """

    # Direct lookup
    if value in mapping:
        return mapping[value]

    # Reverse lookup
    for key, mapped_value in mapping.items():

        if mapped_value == value:
            return key

    # If value is already numeric
    try:
        return int(value)

    except (ValueError, TypeError):
        return 0


# ============================================================
# TASK CATEGORY PREDICTION
# ============================================================

def predict_category(task_description):
    """
    Predict the category of a task using TF-IDF
    and the trained classification model.
    """

    text_vector = tfidf.transform(
        [task_description]
    )

    category = classifier.predict(
        text_vector
    )[0]

    return category


# ============================================================
# PRIORITY PREDICTION
# ============================================================

def predict_priority(
    estimated_hours,
    completed_hours,
    status,
    remaining_hours,
    days_to_deadline,
    category
):
    """
    Predict task priority using the trained
    priority prediction model.

    The model expects exactly these features:

    Estimated_Hours
    Completed_Hours
    Remaining_Hours
    Completion_Percentage
    Days_To_Deadline
    Category_Code
    Status_Code
    """

    # --------------------------------------------------------
    # Calculate completion percentage
    # --------------------------------------------------------

    if estimated_hours > 0:

        completion_percentage = (
            completed_hours /
            estimated_hours
        ) * 100

    else:

        completion_percentage = 0


    # --------------------------------------------------------
    # Convert category into numerical code
    # --------------------------------------------------------

    category_code = get_code_from_mapping(
        category,
        category_mapping
    )


    # --------------------------------------------------------
    # Convert status into numerical code
    # --------------------------------------------------------

    status_code = get_code_from_mapping(
        status,
        status_mapping
    )


    # --------------------------------------------------------
    # Create feature dictionary
    # --------------------------------------------------------

    feature_values = {

        "Estimated_Hours":
            estimated_hours,

        "Completed_Hours":
            completed_hours,

        "Remaining_Hours":
            remaining_hours,

        "Completion_Percentage":
            completion_percentage,

        "Days_To_Deadline":
            days_to_deadline,

        "Category_Code":
            category_code,

        "Status_Code":
            status_code
    }


    # --------------------------------------------------------
    # Arrange features in EXACT training order
    # --------------------------------------------------------

    input_values = []

    for feature in priority_features:

        if feature not in feature_values:

            raise ValueError(
                f"Unknown model feature: {feature}"
            )

        input_values.append(
            feature_values[feature]
        )


    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    input_data = pd.DataFrame(
        [input_values],
        columns=priority_features
    )


    # --------------------------------------------------------
    # Predict priority
    # --------------------------------------------------------

    prediction = priority_model.predict(
        input_data
    )[0]

    return prediction


# ============================================================
# WORKLOAD CALCULATION
# ============================================================

def get_workload():

    """
    Calculate current workload for every team member.
    """

    df = pd.read_csv(
        DATA_PATH
    )


    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    required_columns = [
        "Assigned_To",
        "Task_ID",
        "Estimated_Hours",
        "Completed_Hours"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise ValueError(
                f"Missing column in dataset: {column}"
            )


    # --------------------------------------------------------
    # Calculate workload
    # --------------------------------------------------------

    workload = df.groupby(
        "Assigned_To"
    ).agg(

        Total_Tasks=(
            "Task_ID",
            "count"
        ),

        Estimated_Hours=(
            "Estimated_Hours",
            "sum"
        ),

        Completed_Hours=(
            "Completed_Hours",
            "sum"
        )

    ).reset_index()


    # --------------------------------------------------------
    # Remaining workload
    # --------------------------------------------------------

    workload["Remaining_Hours"] = (

        workload["Estimated_Hours"]

        -

        workload["Completed_Hours"]

    )


    return workload


# ============================================================
# ASSIGNEE RECOMMENDATION
# ============================================================

def recommend_assignee(
    estimated_hours=5
):
    """
    Recommend the team member with the lowest
    projected workload.
    """

    workload = get_workload()


    # --------------------------------------------------------
    # Project workload after assigning new task
    # --------------------------------------------------------

    workload["Projected_Workload"] = (

        workload["Remaining_Hours"]

        +

        estimated_hours

    )


    # --------------------------------------------------------
    # Find lowest workload
    # --------------------------------------------------------

    recommended = workload.loc[
        workload[
            "Projected_Workload"
        ].idxmin()
    ]


    return recommended["Assigned_To"]