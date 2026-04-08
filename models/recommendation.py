import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

def recommendation_score(skill_compatibility, availability_score, department_match, historical_performance):
    return (
        skill_compatibility * 0.4 +
        availability_score * 0.3 +
        department_match * 0.2 +
        historical_performance * 0.1
    )

def calculate_workload_capacity(employee):
    """Calculate available capacity for an employee"""
    max_tasks = 15
    max_hours = 50
    
    task_capacity = (max_tasks - employee['current_tasks']) / max_tasks
    hour_capacity = (max_hours - employee['hours_per_week']) / max_hours
    stress_factor = (10 - employee['stress_indicators']['workload_rating']) / 10
    
    return (task_capacity * 0.4 + hour_capacity * 0.3 + stress_factor * 0.3)

def calculate_skill_match(from_emp, to_emp):
    """Calculate skill compatibility between two employees"""
    # Consider skill level difference
    skill_diff = abs(from_emp['skill_level'] - to_emp['skill_level'])
    skill_score = 1 - (skill_diff / 10)
    
    # Department match
    dept_match = 1.0 if from_emp['department'] == to_emp['department'] else 0.5
    
    # Role compatibility
    role_match = 1.0 if from_emp['role'] == to_emp['role'] else 0.7
    
    return (skill_score * 0.5 + dept_match * 0.3 + role_match * 0.2)

def identify_overloaded_employees(df, threshold=0.7):
    """Identify employees who are overloaded"""
    overloaded = []
    
    for idx, row in df.iterrows():
        # Calculate workload intensity
        task_load = row['current_tasks'] / 15  # Normalized to max 15 tasks
        hour_load = row['hours_per_week'] / 50  # Normalized to max 50 hours
        stress_load = row['stress_indicators']['workload_rating'] / 10
        
        total_load = (task_load + hour_load + stress_load) / 3
        
        if total_load > threshold or row['availability'] == 'Overloaded':
            overloaded.append({
                'employee_id': row['employee_id'],
                'name': row['name'],
                'department': row['department'],
                'load_score': total_load,
                'data': row
            })
    
    return sorted(overloaded, key=lambda x: x['load_score'], reverse=True)

def identify_available_employees(df, threshold=0.5):
    """Identify employees who have capacity to take more work"""
    available = []
    
    for idx, row in df.iterrows():
        capacity = calculate_workload_capacity(row)
        
        if capacity > threshold or row['availability'] == 'Available':
            available.append({
                'employee_id': row['employee_id'],
                'name': row['name'],
                'department': row['department'],
                'capacity_score': capacity,
                'data': row
            })
    
    return sorted(available, key=lambda x: x['capacity_score'], reverse=True)

def recommend_task_redistribution(employee_data):
    """
    AI-powered recommendation system for task redistribution
    Uses ML-based scoring to match overloaded employees with available ones
    """
    if isinstance(employee_data, pd.DataFrame):
        df = employee_data
    else:
        df = pd.DataFrame(employee_data)
    
    recommendations = []
    
    # Identify overloaded and available employees
    overloaded = identify_overloaded_employees(df)
    available = identify_available_employees(df)
    
    if not overloaded or not available:
        return [{
            "message": "No task redistribution needed - workload is balanced",
            "overloaded_count": len(overloaded),
            "available_count": len(available)
        }]
    
    # Generate recommendations
    for overloaded_emp in overloaded[:10]:  # Top 10 overloaded
        best_matches = []
        
        for available_emp in available[:10]:  # Top 10 available
            # Don't recommend self-assignment
            if overloaded_emp['employee_id'] == available_emp['employee_id']:
                continue
            
            # Calculate match score
            skill_match = calculate_skill_match(
                overloaded_emp['data'], 
                available_emp['data']
            )
            
            # Calculate overall recommendation score
            rec_score = recommendation_score(
                skill_compatibility=skill_match,
                availability_score=available_emp['capacity_score'],
                department_match=1.0 if overloaded_emp['department'] == available_emp['department'] else 0.5,
                historical_performance=available_emp['data']['completion_rate']
            )
            
            best_matches.append({
                'to_employee': available_emp,
                'score': rec_score
            })
        
        # Get best match
        if best_matches:
            best_match = max(best_matches, key=lambda x: x['score'])
            
            if best_match['score'] > 0.5:  # Threshold for good match
                # Calculate how many tasks to move
                tasks_to_move = min(
                    int(overloaded_emp['data']['current_tasks'] * 0.3),  # 30% of tasks
                    3  # Max 3 tasks at a time
                )
                
                recommendations.append({
                    "from_employee_id": overloaded_emp['employee_id'],
                    "from_employee_name": overloaded_emp['name'],
                    "from_department": overloaded_emp['department'],
                    "from_workload": overloaded_emp['data']['current_tasks'],
                    "to_employee_id": best_match['to_employee']['employee_id'],
                    "to_employee_name": best_match['to_employee']['name'],
                    "to_department": best_match['to_employee']['department'],
                    "to_capacity": f"{best_match['to_employee']['capacity_score']*100:.0f}%",
                    "recommended_tasks_to_move": tasks_to_move,
                    "match_score": f"{best_match['score']*100:.0f}%",
                    "reason": f"High skill match ({skill_match*100:.0f}%), {best_match['to_employee']['name']} has {best_match['to_employee']['capacity_score']*100:.0f}% capacity",
                    "priority": "High" if overloaded_emp['load_score'] > 0.85 else "Medium"
                })
    
    return recommendations if recommendations else [{
        "message": "No suitable matches found for task redistribution",
        "suggestion": "Consider hiring additional staff or reviewing task priorities"
    }]

def get_task_assignment_recommendation(task_requirements, available_employees_df):
    """
    Recommend best employee for a new task based on skills, capacity, and performance
    """
    if available_employees_df.empty:
        return None
    
    scores = []
    
    for idx, emp in available_employees_df.iterrows():
        # Calculate capacity
        capacity = calculate_workload_capacity(emp)
        
        # Skill level match (assume task_requirements has required_skill_level)
        required_skill = task_requirements.get('required_skill_level', 5)
        skill_score = 1 - abs(emp['skill_level'] - required_skill) / 10
        
        # Department match
        dept_score = 1.0 if emp['department'] == task_requirements.get('department', '') else 0.6
        
        # Performance score
        perf_score = emp['completion_rate']
        
        # Overall score
        overall = (
            skill_score * 0.35 +
            capacity * 0.30 +
            dept_score * 0.20 +
            perf_score * 0.15
        )
        
        scores.append({
            'employee_id': emp['employee_id'],
            'name': emp['name'],
            'score': overall,
            'capacity': capacity,
            'skill_level': emp['skill_level'],
            'department': emp['department']
        })
    
    # Return top 5 recommendations
    top_recommendations = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
    return top_recommendations
