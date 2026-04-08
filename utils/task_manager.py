import json
import pandas as pd
from datetime import datetime
import uuid

def load_tasks():
    """Load tasks from JSON file"""
    try:
        with open("data/tasks.json", "r") as f:
            tasks = json.load(f)
        return pd.DataFrame(tasks) if tasks else pd.DataFrame()
    except:
        return pd.DataFrame()

def save_tasks(tasks_df):
    """Save tasks to JSON file"""
    if isinstance(tasks_df, pd.DataFrame):
        tasks = tasks_df.to_dict('records')
    else:
        tasks = tasks_df
    
    with open("data/tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

def create_task(title, description, assigned_to, assigned_by, priority, estimated_hours, department, skills_required):
    """Create a new task"""
    tasks_df = load_tasks()
    
    new_task = {
        "task_id": str(uuid.uuid4())[:8].upper(),
        "title": title,
        "description": description,
        "assigned_to": assigned_to,
        "assigned_by": assigned_by,
        "status": "Open",
        "priority": priority,
        "estimated_hours": estimated_hours,
        "actual_hours": 0,
        "department": department,
        "skills_required": skills_required,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    if tasks_df.empty:
        tasks_df = pd.DataFrame([new_task])
    else:
        tasks_df = pd.concat([tasks_df, pd.DataFrame([new_task])], ignore_index=True)
    
    save_tasks(tasks_df)
    return new_task

def reassign_task(task_id, new_assignee, reassigned_by):
    """Reassign a task to another employee"""
    tasks_df = load_tasks()
    
    if not tasks_df.empty and task_id in tasks_df['task_id'].values:
        tasks_df.loc[tasks_df['task_id'] == task_id, 'assigned_to'] = new_assignee
        tasks_df.loc[tasks_df['task_id'] == task_id, 'updated_at'] = datetime.now().isoformat()
        tasks_df.loc[tasks_df['task_id'] == task_id, 'reassigned_by'] = reassigned_by
        save_tasks(tasks_df)
        return True
    return False

def update_task_status(task_id, new_status):
    """Update task status"""
    tasks_df = load_tasks()
    
    if not tasks_df.empty and task_id in tasks_df['task_id'].values:
        tasks_df.loc[tasks_df['task_id'] == task_id, 'status'] = new_status
        tasks_df.loc[tasks_df['task_id'] == task_id, 'updated_at'] = datetime.now().isoformat()
        
        if new_status == "Completed":
            tasks_df.loc[tasks_df['task_id'] == task_id, 'completed_at'] = datetime.now().isoformat()
        
        save_tasks(tasks_df)
        return True
    return False

def get_employee_tasks(employee_id):
    """Get all tasks assigned to an employee"""
    tasks_df = load_tasks()
    if not tasks_df.empty and 'assigned_to' in tasks_df.columns:
        return tasks_df[tasks_df['assigned_to'] == employee_id]
    return pd.DataFrame()

def get_department_tasks(department):
    """Get all tasks in a department"""
    tasks_df = load_tasks()
    if not tasks_df.empty and 'department' in tasks_df.columns:
        return tasks_df[tasks_df['department'] == department]
    return pd.DataFrame()
