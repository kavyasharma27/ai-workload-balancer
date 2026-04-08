import json
import random
from datetime import datetime, timedelta

N_EMPLOYEES = 30

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
ROLES = ["Developer", "Manager", "Analyst", "Designer", "QA"]


def random_employee(emp_id):
    name = f"Employee_{emp_id:03d}"
    department = random.choice(DEPARTMENTS)
    role = random.choice(ROLES)
    skill_level = random.randint(1, 10)
    current_tasks = random.randint(3, 15)
    hours_per_week = random.randint(30, 55)
    completion_rate = round(random.uniform(0.7, 1.0), 2)
    overtime_hours = random.randint(0, 15)
    missed_deadlines = random.randint(0, 3)
    workload_rating = random.randint(1, 10)
    availability = random.choice(["Available", "Overloaded", "Underutilized"])
    last_updated = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
    return {
        "employee_id": f"EMP{emp_id:03d}",
        "name": name,
        "department": department,
        "role": role,
        "skill_level": skill_level,
        "current_tasks": current_tasks,
        "hours_per_week": hours_per_week,
        "completion_rate": completion_rate,
        "stress_indicators": {
            "overtime_hours": overtime_hours,
            "missed_deadlines": missed_deadlines,
            "workload_rating": workload_rating
        },
        "availability": availability,
        "last_updated": last_updated
    }


def main():
    employees = [random_employee(i + 1) for i in range(N_EMPLOYEES)]
    with open("data/employees.json", "w") as f:
        json.dump(employees, f, indent=2)
    print(f"Generated {N_EMPLOYEES} synthetic employee records in data/employees.json")

if __name__ == "__main__":
    main()
