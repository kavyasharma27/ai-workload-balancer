import json
import streamlit as st

def load_users():
    """Load users from JSON file"""
    with open("data/users.json", "r") as f:
        return json.load(f)

def authenticate(username, password):
    """Authenticate user and return user data"""
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def is_admin(user):
    """Check if user is admin"""
    return user and user.get("role") == "admin"

def is_manager(user):
    """Check if user is manager"""
    return user and user.get("role") == "manager"

def is_employee(user):
    """Check if user is employee"""
    return user and user.get("role") == "employee"

def get_managed_employees(user):
    """Get list of employees managed by this manager"""
    if is_manager(user):
        return user.get("manages_employees", [])
    return []

def init_session_state():
    """Initialize session state for authentication"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None

def login(user):
    """Log in user"""
    st.session_state.logged_in = True
    st.session_state.user = user

def logout():
    """Log out user"""
    st.session_state.logged_in = False
    st.session_state.user = None
