import pandas as pd
import numpy as np


# =========================================================
# WORKLOAD BALANCER
# =========================================================

DATA_PATH = "data/processed/task_dataset_cleaned.csv"


def load_task_data():
    """
    Load processed task dataset.
    """
    df = pd.read_csv(DATA_PATH)

    return df


def calculate_workload(df):
    """
    Calculate workload for each team member.
    """

    workload = df.groupby("Assigned_To").agg(
        Total_Tasks=("Task_ID", "count"),
        Total_Estimated_Hours=("Estimated_Hours", "sum"),
        Total_Completed_Hours=("Completed_Hours", "sum"),
        Average_Estimated_Hours=("Estimated_Hours", "mean")
    ).reset_index()

    # Remaining work
    workload["Remaining_Hours"] = (
        workload["Total_Estimated_Hours"]
        - workload["Total_Completed_Hours"]
    )

    # Completion percentage
    workload["Completion_Percentage"] = (
        workload["Total_Completed_Hours"]
        /
        workload["Total_Estimated_Hours"].replace(0, 1)
    ) * 100

    return workload


def recommend_assignee(
    workload,
    estimated_hours=5
):
    """
    Recommend the team member with the lowest
    current workload.
    """

    workload = workload.copy()

    # Calculate projected workload
    workload["Projected_Workload"] = (
        workload["Remaining_Hours"]
        + estimated_hours
    )

    # Select member with lowest projected workload
    recommended = workload.loc[
        workload["Projected_Workload"].idxmin()
    ]

    return recommended


def print_workload_report(workload):
    """
    Display workload information.
    """

    print("\n================================")
    print("TEAM WORKLOAD REPORT")
    print("================================")

    print(
        workload[
            [
                "Assigned_To",
                "Total_Tasks",
                "Remaining_Hours",
                "Completion_Percentage"
            ]
        ].to_string(index=False)
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("Loading task data...")

    df = load_task_data()

    print("Dataset loaded successfully.")
    print("Total tasks:", len(df))

    # Calculate workload
    workload = calculate_workload(df)

    # Display report
    print_workload_report(workload)

    # Example new task
    estimated_hours = 5

    recommendation = recommend_assignee(
        workload,
        estimated_hours
    )

    print("\n================================")
    print("TASK ASSIGNMENT RECOMMENDATION")
    print("================================")

    print(
        "Recommended Assignee:",
        recommendation["Assigned_To"]
    )

    print(
        "Current Remaining Hours:",
        round(
            recommendation["Remaining_Hours"],
            2
        )
    )

    print(
        "Projected Workload After Assignment:",
        round(
            recommendation["Projected_Workload"],
            2
        )
    )