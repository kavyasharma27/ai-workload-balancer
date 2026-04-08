# 🚀 AI-Powered Workload Manager Pro

## 📋 Overview

**AI-Powered Workload Manager Pro** is an intelligent enterprise-grade workload management system that uses Machine Learning and AI to optimize task distribution, prevent employee burnout, and maximize team productivity. The system provides role-based dashboards for Admins, Managers, and Employees with real-time analytics, intelligent recommendations, and an AI chatbot assistant.

## ✨ Key Features

### 🤖 **AI & Machine Learning**
- **ML-based Task Recommendation Engine**: Intelligent algorithm that matches tasks to employees based on:
  - Skill compatibility (40% weight)
  - Available capacity (30% weight)
  - Department match (20% weight)
  - Historical performance (10% weight)
- **Predictive Workload Analysis**: Identifies overloaded and available employees automatically
- **AI Chatbot Assistant**: Natural language interface for querying workload data and getting recommendations
- **Smart Task Redistribution**: Automatically suggests optimal task transfers to balance workload

### 👨‍💼 **Admin Dashboard**
- Complete system visibility across all departments
- Real-time analytics and KPI monitoring
- Department-wise performance breakdown
- System-wide task management
- Advanced reporting and visualizations
- User and role management

### 👔 **Manager Dashboard**
- Team workload overview and analytics
- AI-powered task creation with automatic employee recommendations
- Intelligent task redistribution tools
- Team performance tracking
- Department-specific insights
- Task assignment and reassignment capabilities

### 👤 **Employee Dashboard** (Coming Soon)
- Personal task view and management
- Workload tracking
- Performance metrics
- Communication with managers

### 📊 **Advanced Analytics**
- Real-time workload distribution charts
- Department-wise stress heatmaps
- Weekly hours distribution analysis
- Task completion tracking
- Predictive burnout alerts
- Performance trend analysis

### 💬 **AI Chatbot Features**
Ask natural language questions like:
- "Who is overloaded in the Engineering team?"
- "Recommend task assignments for my team"
- "Show me available employees"
- "Give me a status report"
- "Who should I assign this task to?"

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend Layer                    │
│            (Streamlit Web Interface)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Admin   │  │ Manager  │  │ Employee │          │
│  │Dashboard │  │Dashboard │  │Dashboard │          │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│                 Application Layer                    │
│  ┌─────────────────────────────────────────┐        │
│  │         AI Chatbot Engine               │        │
│  │  - NLP Intent Detection                 │        │
│  │  - Context Management                   │        │
│  │  - Response Generation                  │        │
│  └─────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────┐        │
│  │     ML Recommendation Engine            │        │
│  │  - Workload Scoring                     │        │
│  │  - Skill Matching                       │        │
│  │  - Capacity Analysis                    │        │
│  │  - Task Assignment Optimization         │        │
│  └─────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────┐        │
│  │       Authentication & Authorization     │        │
│  │  - Role-based Access Control            │        │
│  │  - Session Management                   │        │
│  └─────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│                   Data Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Employee │  │  Tasks   │  │  Users   │          │
│  │   Data   │  │   Data   │  │ Database │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│          (JSON-based storage)                        │
└─────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### **Backend**
- **Python 3.14**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms
- **SciPy**: Scientific computing

### **Frontend**
- **Streamlit**: Interactive web application framework
- **Plotly**: Advanced data visualizations
- **Plotly Express**: Quick plotting
- **Matplotlib & Seaborn**: Additional visualization support

### **AI/ML Components**
- **Custom ML Recommendation Engine**: Proprietary algorithm for task matching
- **NLP Chatbot**: Intent detection and context-aware responses
- **Predictive Analytics**: Workload forecasting

### **API**
- **Flask**: RESTful API endpoints (optional)

### **Data Storage**
- **JSON**: Lightweight data persistence
- **In-memory processing**: Fast data operations

## 📁 Project Structure

```
WorkLoad_balancer/
│
├── dashboard/
│   └── app.py                    # Main Streamlit application (1000+ lines)
│
├── data/
│   ├── employees.json            # Employee database (30 employees)
│   ├── tasks.json                # Task database (50+ tasks)
│   ├── users.json                # User accounts (admin, managers)
│   ├── generate_synthetic_data.py # Employee data generator
│   └── generate_sample_tasks.py   # Task data generator
│
├── models/
│   ├── classification.py         # ML classification models
│   ├── clustering.py             # Workload clustering algorithms
│   ├── recommendation.py         # AI recommendation engine (200+ lines)
│   └── workload_analysis.py      # Workload scoring algorithms
│
├── utils/
│   ├── auth.py                   # Authentication & authorization
│   ├── data_processing.py        # Data loading and validation
│   ├── task_manager.py           # Task CRUD operations
│   └── ai_chatbot.py             # AI chatbot engine (300+ lines)
│
├── api/
│   └── app.py                    # Flask REST API
│
├── tests/
│   ├── test_data_processing.py   # Data processing tests
│   └── test_workload_analysis.py # Workload analysis tests
│
├── docs/
│   └── architecture.md           # Technical documentation
│
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### **Step 1: Clone or Download Project**
```bash
cd WorkLoad_balancer
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# OR
source venv/bin/activate       # Linux/Mac
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Required packages:**
- pandas >= 1.5.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- scikit-learn >= 1.2.0
- matplotlib >= 3.6.0
- plotly >= 5.14.0
- seaborn >= 0.12.0
- streamlit >= 1.22.0
- flask >= 2.3.0
- python-dotenv >= 1.0.0
- requests >= 2.28.0
- jsonschema >= 4.17.0

### **Step 4: Generate Data (If needed)**
```bash
# Generate employee data
python data/generate_synthetic_data.py

# Generate sample tasks
python data/generate_sample_tasks.py
```

### **Step 5: Run the Application**
```bash
streamlit run dashboard/app.py
```

or

```bash
.\venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

The application will open in your browser at: **http://localhost:8501**

## 👥 Login Credentials

### **Administrator Account**
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system visibility, all departments, system settings

### **Manager Accounts**

**Manager 1 (Engineering Team)**
- **Username**: `manager1`
- **Password**: `manager123`
- **Department**: Engineering
- **Manages**: 10 employees

**Manager 2 (Marketing Team)**
- **Username**: `manager2`
- **Password**: `manager123`
- **Department**: Marketing
- **Manages**: 10 employees

**Manager 3 (Sales Team)**
- **Username**: `manager3`
- **Password**: `manager123`
- **Department**: Sales
- **Manages**: 10 employees

## 📊 How It Works

### **1. Workload Scoring Algorithm**

The system calculates workload scores using the formula:

```python
workload_score = (
    tasks_count × w1 +
    hours_worked × w2 +
    deadline_pressure × w3 +
    complexity_factor × w4
) / skill_level_factor
```

**Variables:**
- `tasks_count`: Number of current tasks (0-15)
- `hours_worked`: Weekly working hours (30-55)
- `deadline_pressure`: Missed deadlines (0-3)
- `complexity_factor`: Workload rating (1-10)
- `skill_level_factor`: Employee skill level (1-10)

### **2. ML Recommendation Engine**

**Task Assignment Recommendation:**
1. **Input**: Task requirements (skills, hours, department)
2. **Analysis**:
   - Calculate employee capacity scores
   - Match skill requirements
   - Check department alignment
   - Review historical performance
3. **Output**: Top 5 recommended employees with match scores

**Task Redistribution Algorithm:**
1. **Identify Overloaded Employees**:
   - Task load > 70% capacity
   - Working hours > 45/week
   - Stress level > 7/10
   - Status = "Overloaded"

2. **Identify Available Employees**:
   - Capacity > 50%
   - Status = "Available"
   - Task load < 10

3. **Match Making**:
   - Calculate skill compatibility
   - Evaluate capacity availability
   - Check department match
   - Score historical performance

4. **Generate Recommendations**:
   - Suggest 30% task transfer (max 3 tasks)
   - Match score > 50% threshold
   - Prioritize high-stress cases

### **3. AI Chatbot Processing**

**Intent Detection:**
- Recommendation queries → Task assignment suggestions
- Overload queries → List overloaded employees
- Availability queries → Show available capacity
- Status queries → Generate reports
- Help queries → Show command list

**Context Awareness:**
- Remembers conversation history
- Filters by user role and department
- Provides role-specific responses

## 🎯 Usage Guide

### **For Administrators**

1. **Login** with admin credentials
2. **Dashboard Views**:
   - **Overview**: System-wide metrics and KPIs
   - **Analytics**: Deep-dive into workload patterns
   - **Employees**: View and filter all 30 employees
   - **All Tasks**: Monitor all 50+ tasks across departments
   - **AI Assistant**: Chat with AI for insights
   - **System Settings**: Configure system parameters

3. **Key Actions**:
   - Monitor department health
   - Review system-wide recommendations
   - Track task completion rates
   - Analyze stress patterns

### **For Managers**

1. **Login** with manager credentials
2. **Dashboard Views**:
   - **Team Overview**: Your 10 team members' workload
   - **Create Task**: AI-assisted task creation
   - **Redistribute Tasks**: Get ML recommendations
   - **Team Tasks**: View and manage team tasks
   - **AI Assistant**: Chat with AI about your team

3. **Creating Tasks**:
   - Enter task details (title, description, hours)
   - Click "Find Best Employee" for AI recommendations
   - View top 5 recommended employees with scores
   - Assign task to chosen employee

4. **Redistributing Tasks**:
   - Click "Generate AI Recommendations"
   - Review suggested task transfers
   - See match scores and capacity details
   - Apply recommendations with one click

5. **Using AI Assistant**:
   - Ask: "Who is overloaded on my team?"
   - Ask: "Who can I assign a new task to?"
   - Ask: "Show team status report"
   - Get instant insights and recommendations

## 🤖 AI Chatbot Commands

### **Workload Queries**
```
"Show me overloaded employees"
"Who is available in Engineering?"
"Give me a status report"
"How is the Marketing team doing?"
```

### **Recommendations**
```
"Recommend task assignments"
"Who should I assign this to?"
"Help me balance the workload"
"Suggest task redistribution"
```

### **Analytics**
```
"Show team capacity"
"What's our completion rate?"
"Who has missed deadlines?"
"Show stress levels"
```

## 📈 Key Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| **Workload Score** | Calculated stress level (0-100+) | < 50 |
| **Availability Status** | Available / Normal / Overloaded | 80% Available |
| **Completion Rate** | Task success rate (0-100%) | > 85% |
| **Stress Level** | Self-reported stress (1-10) | < 7 |
| **Hours/Week** | Working hours | 30-45 hrs |
| **Current Tasks** | Active assignments | 5-10 tasks |
| **Skill Level** | Proficiency rating (1-10) | 5+ |

## 🎨 UI Features

- **Responsive Design**: Works on desktop and tablet
- **Dark Mode Support**: Eye-friendly interface
- **Interactive Charts**: Plotly-powered visualizations
- **Color-coded Status**: Red (overloaded), Green (available), Yellow (normal)
- **Real-time Updates**: Auto-refresh on data changes
- **Expandable Cards**: Detailed employee/task views
- **Search & Filters**: Quick data access
- **Professional Theme**: Modern, clean interface

## 🔐 Security Features

- **Role-based Access Control (RBAC)**
- **Session Management**
- **Password Protection**
- **Department-level Data Isolation**
- **Audit Trail** (planned)

## 📊 Data Models

### **Employee Model**
```json
{
  "employee_id": "EMP001",
  "name": "Employee_001",
  "department": "Engineering",
  "role": "Developer",
  "skill_level": 8,
  "current_tasks": 7,
  "hours_per_week": 42,
  "completion_rate": 0.92,
  "stress_indicators": {
    "overtime_hours": 5,
    "missed_deadlines": 0,
    "workload_rating": 6
  },
  "availability": "Available"
}
```

### **Task Model**
```json
{
  "task_id": "TASK001",
  "title": "Implement authentication",
  "description": "Add OAuth2 login",
  "assigned_to": "EMP001",
  "assigned_by": "mgr001",
  "status": "In Progress",
  "priority": "High",
  "estimated_hours": 16,
  "department": "Engineering",
  "skills_required": "Python, OAuth",
  "created_at": "2026-04-01T10:00:00",
  "updated_at": "2026-04-08T14:30:00"
}
```

## 🚀 Future Enhancements

- [ ] Employee self-service portal
- [ ] Email notifications for task assignments
- [ ] Calendar integration
- [ ] Mobile app (iOS/Android)
- [ ] Advanced ML models (Deep Learning)
- [ ] Predictive burnout prevention
- [ ] Time tracking integration
- [ ] Performance review automation
- [ ] Slack/Teams integration
- [ ] Database backend (PostgreSQL)
- [ ] Multi-language support
- [ ] Custom reporting builder

## 🧪 Testing

Run all tests:
```bash
python -m unittest discover tests
```

Run specific test:
```bash
python -m unittest tests.test_workload_analysis
```

## 🤝 Contributing

This is an enterprise data engineering project. For feature requests or bug reports, please contact the development team.

## 📝 License

Proprietary - All rights reserved

## 👨‍💻 Technical Details

### **Performance**
- Handles 30+ employees efficiently
- Process 50+ tasks in real-time
- ML recommendations in < 1 second
- Dashboard loads in < 2 seconds

### **Scalability**
- Designed for 100+ employees
- Can handle 1000+ concurrent tasks
- Modular architecture for easy scaling
- Database-ready for production

### **Browser Support**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## 📞 Support

For technical support or questions:
- Check documentation in `docs/` folder
- Review code comments
- Use AI Assistant in the application
- Contact system administrator

---

## 🎉 Quick Start Summary

```bash
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run the application
.\venv\Scripts\python.exe -m streamlit run dashboard/app.py

# 3. Login with:
Username: admin
Password: admin123

# 4. Explore features:
- View analytics
- Get AI recommendations
- Chat with AI assistant
- Create and assign tasks
```

**Built with ❤️ for efficient team management and data-driven workforce optimization**
