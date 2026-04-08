import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Import utilities
from utils.data_processing import load_employee_data, validate_employee_data
from utils.auth import authenticate, init_session_state, login, logout, is_admin, is_manager, get_managed_employees
from utils.task_manager import (load_tasks, save_tasks, create_task, reassign_task, 
                                 update_task_status, get_employee_tasks, get_department_tasks)
from utils.ai_chatbot import get_chatbot_response

# Import models
from models.workload_analysis import workload_score
from models.recommendation import recommend_task_redistribution, get_task_assignment_recommendation

# Page configuration
st.set_page_config(
    page_title="AI Workload Manager Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-box {
        padding: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        padding: 10px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
    .danger-box {
        padding: 10px;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def login_page():
    """Display login page"""
    st.markdown('<h1 class="main-header">🚀 AI Workload Manager Pro</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                user = authenticate(username, password)
                if user:
                    login(user)
                    st.success(f"✅ Welcome, {user['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        st.markdown("---")
        st.markdown("""
        ### 🎯 Test Accounts
        
        **Administrator Access:**
        - Username: `admin` | Password: `W0rkl0ad@2026`
        
        **Manager Access:**
        - Engineering: `eng_manager` | Password: `EngMgr@2026`
        - Marketing: `marketing_manager` | Password: `MktMgr@2026`
        - Sales: `sales_manager` | Password: `SalesMgr@2026`
        
        **Employee Access:**
        - Username: `employee` | Password: `Emp@2026`
        
        ### ✨ Key Features
        - 🤖 ML-powered task recommendations
        - 📊 Real-time workforce analytics
        - 🔄 Intelligent workload balancing
        - 💬 AI chatbot assistant
        - 📈 Predictive performance tracking
        """)

def admin_dashboard():
    """Admin dashboard with full system visibility"""
    st.markdown('<h1 class="main-header">👨‍💼 Admin Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_employee_data("data/employees.json")
    tasks_df = load_tasks()
    
    # Calculate workload scores
    df["workload_score"] = df.apply(
        lambda row: workload_score(
            row["current_tasks"],
            row["hours_per_week"],
            row["stress_indicators"]["missed_deadlines"],
            row["stress_indicators"]["workload_rating"],
            row["skill_level"]
        ), axis=1
    )
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Admin Controls")
        st.write(f"**Logged in as:** {st.session_state.user['name']}")
        st.write(f"**Role:** Administrator")
        
        view_option = st.selectbox(
            "Select View",
            ["📊 Overview", "📈 Analytics", "👥 Employees", "📋 All Tasks", "🤖 AI Assistant", "⚙️ System Settings"]
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    if view_option == "📊 Overview":
        show_admin_overview(df, tasks_df)
    elif view_option == "📈 Analytics":
        show_admin_analytics(df, tasks_df)
    elif view_option == "👥 Employees":
        show_all_employees(df)
    elif view_option == "📋 All Tasks":
        show_all_tasks(tasks_df, df)
    elif view_option == "🤖 AI Assistant":
        show_ai_assistant(st.session_state.user)
    elif view_option == "⚙️ System Settings":
        show_system_settings()

def manager_dashboard():
    """Manager dashboard for team management"""
    st.markdown('<h1 class="main-header">👨‍💼 Manager Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_employee_data("data/employees.json")
    tasks_df = load_tasks()
    
    # Filter to manager's team
    managed_employees = get_managed_employees(st.session_state.user)
    team_df = df[df['employee_id'].isin(managed_employees)]
    
    # Calculate workload scores
    team_df["workload_score"] = team_df.apply(
        lambda row: workload_score(
            row["current_tasks"],
            row["hours_per_week"],
            row["stress_indicators"]["missed_deadlines"],
            row["stress_indicators"]["workload_rating"],
            row["skill_level"]
        ), axis=1
    )
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Manager Controls")
        st.write(f"**Logged in as:** {st.session_state.user['name']}")
        st.write(f"**Department:** {st.session_state.user['department']}")
        st.write(f"**Team Size:** {len(team_df)} employees")
        
        view_option = st.selectbox(
            "Select View",
            ["📊 Team Overview", "➕ Create Task", "🔄 Redistribute Tasks", "📋 Team Tasks", "🤖 AI Assistant"]
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    if view_option == "📊 Team Overview":
        show_team_overview(team_df, managed_employees)
    elif view_option == "➕ Create Task":
        show_create_task(team_df, st.session_state.user)
    elif view_option == "🔄 Redistribute Tasks":
        show_redistribute_tasks(team_df)
    elif view_option == "📋 Team Tasks":
        show_team_tasks(tasks_df, managed_employees)
    elif view_option == "🤖 AI Assistant":
        show_ai_assistant(st.session_state.user)

def employee_dashboard():
    """Employee dashboard for personal task view"""
    st.markdown('<h1 class="main-header">👤 Employee Dashboard</h1>', unsafe_allow_html=True)
    
    st.info("🚧 Employee login feature coming soon! For now, please use Admin or Manager accounts.")
    
    if st.button("← Back to Login"):
        logout()
        st.rerun()

def show_admin_overview(df, tasks_df):
    """Show admin overview metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Employees", len(df))
    with col2:
        overloaded = len(df[df['availability'] == 'Overloaded'])
        st.metric("🔴 Overloaded", overloaded, delta=f"{overloaded/len(df)*100:.1f}%")
    with col3:
        total_tasks = len(tasks_df) if not tasks_df.empty else 0
        st.metric("📋 Total Tasks", total_tasks)
    with col4:
        avg_workload = df['current_tasks'].mean()
        st.metric("📊 Avg Tasks/Person", f"{avg_workload:.1f}")
    
    st.markdown("---")
    
    # Department breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Department Distribution")
        dept_counts = df['department'].value_counts()
        fig = px.pie(values=dept_counts.values, names=dept_counts.index, 
                     title="Employees by Department", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⚡ Workload Status")
        status_counts = df['availability'].value_counts()
        colors = {'Overloaded': '#dc3545', 'Available': '#28a745', 'Underutilized': '#ffc107'}
        fig = px.bar(x=status_counts.index, y=status_counts.values,
                     title="Employee Availability Status",
                     color=status_counts.index,
                     color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Recommendations
    st.markdown("### 🤖 AI Recommendations")
    if st.button("🔄 Generate Recommendations", use_container_width=True):
        with st.spinner("Analyzing workload patterns..."):
            recs = recommend_task_redistribution(df)
            
            if recs and 'message' not in recs[0]:
                for rec in recs[:5]:
                    with st.expander(f"⚠️ {rec['priority']} Priority: {rec['from_employee_name']} → {rec['to_employee_name']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**From:** {rec['from_employee_name']}")
                            st.write(f"**Department:** {rec['from_department']}")
                            st.write(f"**Current Workload:** {rec['from_workload']} tasks")
                        with col2:
                            st.write(f"**To:** {rec['to_employee_name']}")
                            st.write(f"**Capacity:** {rec['to_capacity']}")
                            st.write(f"**Match Score:** {rec['match_score']}")
                        st.info(f"**Recommendation:** Move {rec['recommended_tasks_to_move']} tasks")
                        st.write(f"**Reason:** {rec['reason']}")
            else:
                st.success("✅ Workload is well balanced across all teams!")

def show_admin_analytics(df, tasks_df):
    """Show detailed analytics"""
    st.markdown("### 📈 Workload Analytics")
    
    # Workload score distribution
    fig = px.box(df, x='department', y='workload_score', 
                 title="Workload Score Distribution by Department",
                 color='department')
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Stress Heatmap")
        stress_data = df.groupby('department')['stress_indicators'].apply(
            lambda x: x.apply(lambda y: y['workload_rating']).mean()
        )
        fig = go.Figure(data=go.Bar(x=stress_data.index, y=stress_data.values,
                                     marker_color=stress_data.values,
                                     marker_colorscale='Reds'))
        fig.update_layout(title="Average Stress Level by Department",
                         xaxis_title="Department",
                         yaxis_title="Stress Level (1-10)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⏰ Hours Distribution")
        fig = px.histogram(df, x='hours_per_week', nbins=20,
                          title="Weekly Hours Distribution",
                          color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig, use_container_width=True)

def show_all_employees(df):
    """Show all employees with details"""
    st.markdown("### 👥 All Employees")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        dept_filter = st.multiselect("Filter by Department", df['department'].unique())
    with col2:
        role_filter = st.multiselect("Filter by Role", df['role'].unique())
    with col3:
        status_filter = st.multiselect("Filter by Status", df['availability'].unique())
    
    # Apply filters
    filtered_df = df.copy()
    if dept_filter:
        filtered_df = filtered_df[filtered_df['department'].isin(dept_filter)]
    if role_filter:
        filtered_df = filtered_df[filtered_df['role'].isin(role_filter)]
    if status_filter:
        filtered_df = filtered_df[filtered_df['availability'].isin(status_filter)]
    
    # Display table
    display_cols = ['employee_id', 'name', 'department', 'role', 'skill_level', 
                    'current_tasks', 'hours_per_week', 'completion_rate', 'availability']
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=600)

def show_all_tasks(tasks_df, df):
    """Show all tasks in system"""
    st.markdown("### 📋 All Tasks")
    
    if tasks_df.empty:
        st.info("📝 No tasks in the system yet. Managers can create tasks from their dashboard.")
        return
    
    # Task statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tasks", len(tasks_df))
    with col2:
        open_tasks = len(tasks_df[tasks_df['status'] == 'Open'])
        st.metric("Open Tasks", open_tasks)
    with col3:
        in_progress = len(tasks_df[tasks_df['status'] == 'In Progress'])
        st.metric("In Progress", in_progress)
    with col4:
        completed = len(tasks_df[tasks_df['status'] == 'Completed'])
        st.metric("Completed", completed)
    
    st.dataframe(tasks_df, use_container_width=True)

def show_team_overview(team_df, managed_employees):
    """Show team overview for managers"""
    st.markdown(f"### 👥 Your Team ({len(team_df)} members)")
    
    # Team metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Team Size", len(team_df))
    with col2:
        overloaded = len(team_df[team_df['availability'] == 'Overloaded'])
        st.metric("Overloaded", overloaded)
    with col3:
        avg_tasks = team_df['current_tasks'].mean()
        st.metric("Avg Tasks", f"{avg_tasks:.1f}")
    with col4:
        avg_completion = team_df['completion_rate'].mean()
        st.metric("Avg Completion", f"{avg_completion*100:.0f}%")
    
    st.markdown("---")
    
    # Team workload chart
    fig = px.bar(team_df, x='name', y='workload_score',
                 title="Team Workload Scores",
                 color='availability',
                 color_discrete_map={'Overloaded': '#dc3545', 'Available': '#28a745'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Team members details
    st.markdown("### 📊 Team Members")
    for idx, emp in team_df.iterrows():
        with st.expander(f"{emp['name']} - {emp['role']} ({emp['availability']})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**ID:** {emp['employee_id']}")
                st.write(f"**Skill Level:** {emp['skill_level']}/10")
                st.write(f"**Completion Rate:** {emp['completion_rate']*100:.0f}%")
            with col2:
                st.write(f"**Current Tasks:** {emp['current_tasks']}")
                st.write(f"**Hours/Week:** {emp['hours_per_week']}")
                st.write(f"**Overtime:** {emp['stress_indicators']['overtime_hours']} hrs")
            with col3:
                st.write(f"**Stress Level:** {emp['stress_indicators']['workload_rating']}/10")
                st.write(f"**Missed Deadlines:** {emp['stress_indicators']['missed_deadlines']}")
                st.write(f"**Status:** {emp['availability']}")

def show_create_task(team_df, manager):
    """Show task creation interface"""
    st.markdown("### ➕ Create New Task")
    
    with st.form("create_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title*", placeholder="e.g., Implement user authentication")
            task_priority = st.selectbox("Priority*", ["High", "Medium", "Low"])
            estimated_hours = st.number_input("Estimated Hours*", min_value=1, max_value=100, value=8)
        
        with col2:
            task_description = st.text_area("Description*", placeholder="Detailed task description...", height=100)
            skills_required = st.text_input("Skills Required", placeholder="e.g., Python, React, SQL")
        
        st.markdown("---")
        st.markdown("#### 🤖 AI-Powered Assignment Recommendation")
        
        if st.form_submit_button("🔍 Find Best Employee", use_container_width=True):
            if task_title and estimated_hours:
                # Get AI recommendations
                task_req = {
                    'required_skill_level': 7,
                    'department': manager['department'],
                    'estimated_hours': estimated_hours
                }
                
                recommendations = get_task_assignment_recommendation(task_req, team_df)
                
                if recommendations:
                    st.success("🎯 Top Recommendations:")
                    for i, rec in enumerate(recommendations, 1):
                        st.write(f"{i}. **{rec['name']}** - Score: {rec['score']*100:.0f}% "
                                f"(Capacity: {rec['capacity']*100:.0f}%, Skill: {rec['skill_level']}/10)")
        
        st.markdown("---")
        assign_to = st.selectbox("Assign To*", 
                                 options=team_df['employee_id'].tolist(),
                                 format_func=lambda x: team_df[team_df['employee_id']==x]['name'].values[0] if len(team_df[team_df['employee_id']==x]) > 0 else x)
        
        submitted = st.form_submit_button("✅ Create Task", use_container_width=True, type="primary")
        
        if submitted:
            if task_title and task_description and assign_to:
                new_task = create_task(
                    title=task_title,
                    description=task_description,
                    assigned_to=assign_to,
                    assigned_by=manager['user_id'],
                    priority=task_priority,
                    estimated_hours=estimated_hours,
                    department=manager['department'],
                    skills_required=skills_required
                )
                st.success(f"✅ Task created successfully! Task ID: {new_task['task_id']}")
                st.balloons()
            else:
                st.error("❌ Please fill in all required fields (*)")

def show_redistribute_tasks(team_df):
    """Show task redistribution interface"""
    st.markdown("### 🔄 Intelligent Task Redistribution")
    
    if st.button("🤖 Generate AI Recommendations", use_container_width=True):
        with st.spinner("Analyzing team workload..."):
            recs = recommend_task_redistribution(team_df)
            
            if recs and 'message' not in recs[0]:
                st.success(f"✅ Found {len(recs)} optimization opportunities!")
                
                for i, rec in enumerate(recs, 1):
                    with st.expander(f"#{i} - {rec['priority']} Priority: {rec['from_employee_name']} → {rec['to_employee_name']}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**From:** {rec['from_employee_name']} ({rec['from_department']})")
                            st.markdown(f"**Current Workload:** {rec['from_workload']} tasks")
                            st.markdown(f"**To:** {rec['to_employee_name']} ({rec['to_department']})")
                            st.markdown(f"**Available Capacity:** {rec['to_capacity']}")
                            st.markdown(f"**Match Quality:** {rec['match_score']}")
                            st.info(f"💡 {rec['reason']}")
                        
                        with col2:
                            st.metric("Tasks to Move", rec['recommended_tasks_to_move'])
                            if st.button(f"✅ Apply", key=f"apply_{i}", use_container_width=True):
                                st.success("Task redistribution applied!")
                                # Here you would call the reassign_task function
            else:
                st.success("✅ Your team's workload is perfectly balanced! No changes needed.")

def show_team_tasks(tasks_df, managed_employees):
    """Show tasks for manager's team"""
    st.markdown("### 📋 Team Tasks")
    
    if tasks_df.empty:
        st.info("📝 No tasks yet. Create your first task using the '➕ Create Task' view!")
        return
    
    # Filter to manager's team
    team_tasks = tasks_df[tasks_df['assigned_to'].isin(managed_employees)]
    
    if team_tasks.empty:
        st.info("📝 No tasks assigned to your team members yet.")
        return
    
    # Task filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Open", "In Progress", "Completed"])
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    with col3:
        assignee_filter = st.selectbox("Assignee", ["All"] + managed_employees)
    
    # Apply filters
    filtered_tasks = team_tasks.copy()
    if status_filter != "All":
        filtered_tasks = filtered_tasks[filtered_tasks['status'] == status_filter]
    if priority_filter != "All":
        filtered_tasks = filtered_tasks[filtered_tasks['priority'] == priority_filter]
    if assignee_filter != "All":
        filtered_tasks = filtered_tasks[filtered_tasks['assigned_to'] == assignee_filter]
    
    # Display tasks
    st.dataframe(filtered_tasks, use_container_width=True)

def show_ai_assistant(user):
    """Show AI chatbot assistant"""
    st.markdown("### 🤖 AI Workload Assistant")
    
    st.info("💬 Ask me about workload, task assignments, team status, and recommendations!")
    
    # Chat input
    user_input = st.text_input("Your message:", placeholder="Type your question here...", key="chat_input")
    
    if st.button("Send", use_container_width=True) and user_input:
        # Get AI response
        response = get_chatbot_response(user_input, user)
        
        # Add to chat history
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        st.session_state.chat_history.append({"role": "assistant", "message": response})
    
    # Display chat history
    st.markdown("---")
    st.markdown("### 💬 Conversation")
    
    for chat in st.session_state.chat_history[-10:]:  # Show last 10 messages
        if chat["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 {chat["message"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 {chat["message"]}</div>', 
                       unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

def show_system_settings():
    """Show system settings"""
    st.markdown("### ⚙️ System Settings")
    
    st.info("🚧 Advanced settings and configurations coming soon!")
    
    st.markdown("#### 🔧 Current Configuration")
    st.json({
        "system_version": "2.0.0",
        "ml_model": "Active",
        "ai_chatbot": "Enabled",
        "total_users": 3,
        "total_employees": 30
    })

# Main application logic
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        user = st.session_state.user
        
        if is_admin(user):
            admin_dashboard()
        elif is_manager(user):
            manager_dashboard()
        else:
            employee_dashboard()

if __name__ == "__main__":
    main()
