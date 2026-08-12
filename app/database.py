import sqlite3
import os
import pandas as pd


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "task_management.db"
)


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            task_description TEXT NOT NULL,

            category TEXT,

            priority TEXT,

            estimated_hours REAL,

            completed_hours REAL,

            remaining_hours REAL,

            days_to_deadline INTEGER,

            status TEXT,

            assigned_to TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE TASK
# ============================================================

def save_task(
    task_description,
    category,
    priority,
    estimated_hours,
    completed_hours,
    remaining_hours,
    days_to_deadline,
    status,
    assigned_to
):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (

            task_description,
            category,
            priority,
            estimated_hours,
            completed_hours,
            remaining_hours,
            days_to_deadline,
            status,
            assigned_to

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            task_description,
            category,
            priority,
            estimated_hours,
            completed_hours,
            remaining_hours,
            days_to_deadline,
            status,
            assigned_to
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET ALL TASKS
# ============================================================

def get_tasks():

    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM tasks
        ORDER BY created_at DESC
        """,
        connection
    )

    connection.close()

    return df


# ============================================================
# GET STATISTICS
# ============================================================

def get_statistics():

    connection = sqlite3.connect(DB_PATH)

    total_tasks = pd.read_sql_query(
        "SELECT COUNT(*) AS count FROM tasks",
        connection
    ).iloc[0]["count"]

    priority_data = pd.read_sql_query(
        """
        SELECT priority, COUNT(*) AS count
        FROM tasks
        GROUP BY priority
        """,
        connection
    )

    category_data = pd.read_sql_query(
        """
        SELECT category, COUNT(*) AS count
        FROM tasks
        GROUP BY category
        """,
        connection
    )

    assignee_data = pd.read_sql_query(
        """
        SELECT assigned_to, COUNT(*) AS count
        FROM tasks
        GROUP BY assigned_to
        """,
        connection
    )

    connection.close()

    return (
        total_tasks,
        priority_data,
        category_data,
        assignee_data
    )