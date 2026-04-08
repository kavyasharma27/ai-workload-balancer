import json
import random
from datetime import datetime, timedelta

TASK_TITLES = [
    "Implement user authentication system",
    "Design database schema for new features",
    "Fix critical production bug in payment module",
    "Optimize SQL query performance",
    "Create REST API endpoints for mobile app",
    "Write unit tests for core modules",
    "Update documentation for API changes",
    "Refactor legacy codebase",
    "Implement real-time notifications",
    "Design UI mockups for dashboard",
    "Conduct code review for pull requests",
    "Set up CI/CD pipeline",
    "Analyze user feedback and create report",
    "Implement data export functionality",
    "Upgrade to latest framework version",
    "Create marketing campaign for Q2",
    "Optimize website loading speed",
    "Implement A/B testing framework",
    "Design email templates",
    "Create sales presentation deck",
    "Conduct customer satisfaction survey",
    "Implement multi-factor authentication",
    "Create data visualization dashboard",
    "Optimize cloud infrastructure costs",
    "Implement automated backup system",
    "Create training materials for new hires",
    "Conduct security audit",
    "Implement search functionality",
    "Create mobile app prototype",
    "Design landing page for new product"
]

DESCRIPTIONS = [
    "High priority task that needs immediate attention",
    "Medium priority - complete within this sprint",
    "Low priority - can be scheduled for next sprint",
    "Critical bug fix required for production stability",
    "Feature enhancement requested by product team",
    "Technical debt cleanup and optimization",
    "Customer-requested feature implementation",
    "Internal process improvement initiative",
    "Compliance and security requirement",
    "Performance optimization task"
]

STATUSES = ["Open", "In Progress", "Completed"]
PRIORITIES = ["High", "Medium", "Low"]
DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
SKILLS = ["Python, Django", "React, JavaScript", "SQL, Database Design", "AWS, DevOps", 
          "UI/UX Design", "Data Analysis", "Marketing Strategy", "Sales Operations"]

# Manager mappings
MANAGER_EMPLOYEES = {
    "mgr001": ["EMP001", "EMP004", "EMP007", "EMP010", "EMP013", "EMP016", "EMP019", "EMP022", "EMP025", "EMP028"],
    "mgr002": ["EMP002", "EMP005", "EMP008", "EMP011", "EMP014", "EMP017", "EMP020", "EMP023", "EMP026", "EMP029"],
    "mgr003": ["EMP003", "EMP006", "EMP009", "EMP012", "EMP015", "EMP018", "EMP021", "EMP024", "EMP027", "EMP030"]
}

def generate_sample_tasks(num_tasks=50):
    """Generate sample tasks for the system"""
    tasks = []
    
    for i in range(num_tasks):
        manager_id = random.choice(list(MANAGER_EMPLOYEES.keys()))
        employee_id = random.choice(MANAGER_EMPLOYEES[manager_id])
        
        status = random.choice(STATUSES)
        created_date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        task = {
            "task_id": f"TASK{i+1:03d}",
            "title": random.choice(TASK_TITLES),
            "description": random.choice(DESCRIPTIONS),
            "assigned_to": employee_id,
            "assigned_by": manager_id,
            "status": status,
            "priority": random.choice(PRIORITIES),
            "estimated_hours": random.randint(4, 40),
            "actual_hours": random.randint(0, 35) if status != "Open" else 0,
            "department": random.choice(DEPARTMENTS),
            "skills_required": random.choice(SKILLS),
            "created_at": created_date.isoformat(),
            "updated_at": (created_date + timedelta(days=random.randint(0, 10))).isoformat(),
            "completed_at": (created_date + timedelta(days=random.randint(5, 20))).isoformat() if status == "Completed" else None
        }
        
        tasks.append(task)
    
    return tasks

def main():
    # Generate tasks
    tasks = generate_sample_tasks(50)
    
    # Save to file
    with open("data/tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
    
    print(f"✅ Generated {len(tasks)} sample tasks in data/tasks.json")
    
    # Print statistics
    statuses = {}
    priorities = {}
    for task in tasks:
        statuses[task['status']] = statuses.get(task['status'], 0) + 1
        priorities[task['priority']] = priorities.get(task['priority'], 0) + 1
    
    print(f"\n📊 Task Statistics:")
    print(f"   Status: {statuses}")
    print(f"   Priority: {priorities}")

if __name__ == "__main__":
    main()
