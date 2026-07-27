from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os

fake = Faker()

# Categories
categories = [
    "Bug",
    "Feature",
    "Documentation",
    "Testing",
    "Database",
    "UI/UX",
    "Backend",
    "Frontend",
    "DevOps",
    "Security"
]

# Priorities
priorities = ["Low", "Medium", "High", "Critical"]

# Status
statuses = [
    "Pending",
    "In Progress",
    "Completed",
    "On Hold"
]

# Team Members
team_members = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Emma",
    "Frank",
    "Grace",
    "Henry"
]

# Task descriptions
task_descriptions = [
    "Fix login authentication bug",
    "Design dashboard UI",
    "Implement payment gateway",
    "Create REST API",
    "Optimize SQL queries",
    "Write unit tests",
    "Develop user profile page",
    "Improve application performance",
    "Implement dark mode",
    "Deploy application",
    "Integrate email notifications",
    "Refactor backend code",
    "Build admin panel",
    "Add search functionality",
    "Create reports module",
    "Fix responsive layout",
    "Update project documentation",
    "Implement chatbot",
    "Develop analytics dashboard",
    "Configure CI/CD pipeline"
]

records = []

for i in range(1, 10001):

    created_date = fake.date_between(start_date='-180d', end_date='today')

    deadline = created_date + timedelta(days=random.randint(2, 30))

    estimated_hours = random.randint(1, 20)

    completed_hours = random.randint(0, estimated_hours)

    record = {
        "Task_ID": f"TASK_{i:05d}",
        "Task_Description": random.choice(task_descriptions),
        "Category": random.choice(categories),
        "Priority": random.choice(priorities),
        "Assigned_To": random.choice(team_members),
        "Status": random.choice(statuses),
        "Estimated_Hours": estimated_hours,
        "Completed_Hours": completed_hours,
        "Created_Date": created_date,
        "Deadline": deadline
    }

    records.append(record)

df = pd.DataFrame(records)

# Create folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Save CSV
df.to_csv("data/raw/task_dataset.csv", index=False)

print("Dataset Created Successfully!")
print(df.head())