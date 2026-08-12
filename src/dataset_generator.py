from faker import Faker
import pandas as pd
import random
import os
from datetime import timedelta

fake = Faker()

# ---------------------------------------------------------
# Task templates grouped by category
# ---------------------------------------------------------

task_templates = {
    "Bug": [
        "Fix application crash on login",
        "Resolve incorrect task status display",
        "Fix broken notification functionality",
        "Fix error in task creation workflow",
        "Resolve duplicate task issue",
        "Fix incorrect user permissions",
        "Resolve dashboard loading error",
        "Fix task assignment failure"
    ],

    "Feature": [
        "Implement task creation feature",
        "Add task filtering functionality",
        "Implement task search feature",
        "Add recurring tasks",
        "Implement task reminder feature",
        "Add team member assignment",
        "Implement task comments",
        "Add task history tracking"
    ],

    "Documentation": [
        "Update API documentation",
        "Write user guide",
        "Document project architecture",
        "Update installation instructions",
        "Create developer documentation",
        "Document database schema",
        "Update README documentation",
        "Create deployment guide"
    ],

    "Testing": [
        "Write unit tests for authentication",
        "Create integration tests",
        "Test task creation workflow",
        "Perform API endpoint testing",
        "Create regression test cases",
        "Test user permissions",
        "Perform dashboard testing",
        "Create automated test suite"
    ],

    "Database": [
        "Optimize SQL queries",
        "Design task management database",
        "Create database indexes",
        "Fix database connection issue",
        "Optimize database performance",
        "Create task database tables",
        "Implement database backup",
        "Update database schema"
    ],

    "UI/UX": [
        "Design task management dashboard",
        "Improve navigation layout",
        "Create responsive task interface",
        "Design login page",
        "Improve dashboard user experience",
        "Implement dark mode",
        "Redesign task details page",
        "Improve mobile interface"
    ],

    "Backend": [
        "Develop task management API",
        "Implement authentication API",
        "Create task assignment service",
        "Develop user management API",
        "Implement task notification service",
        "Create backend validation",
        "Develop reporting API",
        "Implement task workflow service"
    ],

    "Frontend": [
        "Develop task dashboard",
        "Create task creation form",
        "Build user profile interface",
        "Implement task filtering UI",
        "Create task details component",
        "Develop team management page",
        "Build notification interface",
        "Create responsive frontend"
    ],

    "DevOps": [
        "Configure CI/CD pipeline",
        "Deploy application to server",
        "Configure Docker environment",
        "Set up application monitoring",
        "Configure cloud deployment",
        "Automate deployment process",
        "Configure GitHub Actions",
        "Set up production environment"
    ],

    "Security": [
        "Fix authentication vulnerability",
        "Implement secure password storage",
        "Add role based access control",
        "Perform security audit",
        "Implement API authentication",
        "Fix authorization issue",
        "Add input validation security",
        "Improve application security"
    ]
}

categories = list(task_templates.keys())

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

statuses = [
    "Pending",
    "In Progress",
    "Completed",
    "On Hold"
]

records = []

# ---------------------------------------------------------
# Generate 10,000 realistic task records
# ---------------------------------------------------------

for i in range(1, 10001):

    # Select category first
    category = random.choice(categories)

    # Select a description belonging to that category
    description = random.choice(task_templates[category])

    # Generate creation date
    created_date = fake.date_between(
        start_date="-180d",
        end_date="today"
    )

    # Generate deadline
    deadline = created_date + timedelta(
        days=random.randint(2, 30)
    )

    # Calculate estimated effort
    estimated_hours = random.randint(1, 20)

    # Completed hours cannot exceed estimated hours
    completed_hours = random.randint(
        0,
        estimated_hours
    )

    # -----------------------------------------------------
    # Priority logic
    # -----------------------------------------------------

    if category in ["Security", "Bug"]:
        priority = random.choices(
            ["Medium", "High", "Critical"],
            weights=[20, 50, 30],
            k=1
        )[0]

    elif category in ["DevOps", "Database", "Backend"]:
        priority = random.choices(
            ["Low", "Medium", "High"],
            weights=[10, 40, 50],
            k=1
        )[0]

    else:
        priority = random.choices(
            ["Low", "Medium", "High"],
            weights=[30, 50, 20],
            k=1
        )[0]

    record = {
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
    }

    records.append(record)

# ---------------------------------------------------------
# Create DataFrame
# ---------------------------------------------------------

df = pd.DataFrame(records)

# Create output directory
os.makedirs("data/raw", exist_ok=True)

# Save dataset
output_path = "data/raw/task_dataset.csv"

df.to_csv(
    output_path,
    index=False
)

print("Dataset Created Successfully!")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Saved to: {output_path}")

print("\nCategory distribution:")
print(df["Category"].value_counts())

print("\nPriority distribution:")
print(df["Priority"].value_counts())

print("\nFirst 5 records:")
print(df.head())