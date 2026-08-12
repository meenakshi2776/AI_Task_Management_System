from faker import Faker
import pandas as pd
import random
import os
from datetime import timedelta

fake = Faker()

# ---------------------------------------------------------
# Task descriptions by category
# ---------------------------------------------------------

task_templates = {
    "Bug": [
        "Fix {system} crash affecting {feature}",
        "Resolve {feature} error in the {system}",
        "Investigate unexpected failure in {feature}",
        "Repair broken {feature} functionality",
        "Fix incorrect {feature} behavior",
        "Resolve application error during {feature}"
    ],

    "Feature": [
        "Implement new {feature} functionality",
        "Add {feature} to the application",
        "Develop a new {feature} module",
        "Create functionality for {feature}",
        "Introduce {feature} support",
        "Build the {feature} feature"
    ],

    "Documentation": [
        "Update documentation for {feature}",
        "Create user documentation for {feature}",
        "Write developer guide for {feature}",
        "Document the {feature} workflow",
        "Update README with {feature} instructions",
        "Prepare technical documentation for {feature}"
    ],

    "Testing": [
        "Write unit tests for {feature}",
        "Perform integration testing for {feature}",
        "Create test cases for {feature}",
        "Validate {feature} functionality",
        "Perform regression testing on {feature}",
        "Automate testing for {feature}"
    ],

    "Database": [
        "Optimize database queries for {feature}",
        "Update database schema for {feature}",
        "Create database tables for {feature}",
        "Improve database performance for {feature}",
        "Fix database connection for {feature}",
        "Add database indexes for {feature}"
    ],

    "UI/UX": [
        "Improve user interface for {feature}",
        "Redesign {feature} screen",
        "Improve user experience of {feature}",
        "Create responsive design for {feature}",
        "Update visual layout of {feature}",
        "Improve navigation for {feature}"
    ],

    "Backend": [
        "Develop backend API for {feature}",
        "Implement server-side logic for {feature}",
        "Create backend service for {feature}",
        "Add API support for {feature}",
        "Improve backend processing for {feature}",
        "Implement business logic for {feature}"
    ],

    "Frontend": [
        "Develop frontend interface for {feature}",
        "Create frontend component for {feature}",
        "Build user interface for {feature}",
        "Implement frontend functionality for {feature}",
        "Develop responsive page for {feature}",
        "Update frontend workflow for {feature}"
    ],

    "DevOps": [
        "Configure deployment for {feature}",
        "Set up CI/CD pipeline for {feature}",
        "Deploy {feature} to production",
        "Configure monitoring for {feature}",
        "Automate deployment of {feature}",
        "Set up cloud environment for {feature}"
    ],

    "Security": [
        "Fix security vulnerability in {feature}",
        "Improve authentication for {feature}",
        "Implement access control for {feature}",
        "Secure {feature} against unauthorized access",
        "Perform security audit for {feature}",
        "Improve data protection for {feature}"
    ]
}

features = [
    "login",
    "task management",
    "user authentication",
    "dashboard",
    "notifications",
    "reporting",
    "search",
    "user profile",
    "team management",
    "task assignment",
    "analytics",
    "file upload",
    "API integration",
    "payment processing",
    "email notifications"
]

team_members = [
    "Alice", "Bob", "Charlie", "David",
    "Emma", "Frank", "Grace", "Henry"
]

statuses = [
    "Pending",
    "In Progress",
    "Completed",
    "On Hold"
]

records = []

# ---------------------------------------------------------
# Generate 10,000 tasks
# ---------------------------------------------------------

for i in range(1, 10001):

    category = random.choice(list(task_templates.keys()))

    feature = random.choice(features)

    template = random.choice(task_templates[category])

    description = template.format(feature=feature, system="application")

    created_date = fake.date_between(
        start_date="-180d",
        end_date="today"
    )

    deadline = created_date + timedelta(
        days=random.randint(2, 30)
    )

    estimated_hours = random.randint(1, 20)

    completed_hours = random.randint(
        0,
        estimated_hours
    )

    # Priority based on category
    if category in ["Security", "Bug"]:
        priority = random.choices(
            ["Medium", "High", "Critical"],
            weights=[25, 50, 25]
        )[0]

    elif category in ["DevOps", "Database", "Backend"]:
        priority = random.choices(
            ["Low", "Medium", "High"],
            weights=[15, 45, 40]
        )[0]

    else:
        priority = random.choices(
            ["Low", "Medium", "High"],
            weights=[30, 50, 20]
        )[0]

    records.append({
        "Task_ID": f"TASK_{i:05d}",
        "Task_Description": description,
        "Category": category,
        "Priority": priority,
        "Assigned_To": random.choice(team_members),
        "Status": random.choice(statuses),
        "Estimated_Hours": estimated_hours,
        "Completed_Hours": completed_hours,
        "Created_Date": created_date,
        "Deadline": deadline
    })

df = pd.DataFrame(records)

os.makedirs("data/raw", exist_ok=True)

df.to_csv(
    "data/raw/task_dataset.csv",
    index=False
)

print("Dataset Created Successfully!")
print("Total records:", len(df))
print("Total columns:", len(df.columns))

print("\nCategory Distribution:")
print(df["Category"].value_counts())

print("\nPriority Distribution:")
print(df["Priority"].value_counts())

print("\nSample Tasks:")
print(df[["Task_Description", "Category", "Priority"]].head(10))