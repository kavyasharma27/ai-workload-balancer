import json
import re
from datetime import datetime
from utils.data_processing import load_employee_data
from utils.task_manager import load_tasks, create_task, reassign_task, get_employee_tasks
from models.recommendation import recommend_task_redistribution, get_task_assignment_recommendation

class WorkloadAIChatbot:
    """AI Chatbot for workload management and task assignment"""
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
    
    def process_message(self, user_message, user_data=None):
        """Process user message and return AI response"""
        message_lower = user_message.lower()
        
        # Store conversation
        self.conversation_history.append({
            "user": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Intent detection
        if any(word in message_lower for word in ["recommend", "suggest", "who should", "assign"]):
            response = self._handle_recommendation_query(user_message, user_data)
        
        elif any(word in message_lower for word in ["overload", "busy", "too much work", "stressed"]):
            response = self._handle_overload_query(user_data)
        
        elif any(word in message_lower for word in ["available", "free", "capacity", "can take"]):
            response = self._handle_availability_query(user_data)
        
        elif any(word in message_lower for word in ["balance", "redistribute", "move tasks"]):
            response = self._handle_balance_query(user_data)
        
        elif any(word in message_lower for word in ["status", "workload", "how is", "report"]):
            response = self._handle_status_query(user_data)
        
        elif any(word in message_lower for word in ["create task", "new task", "add task"]):
            response = self._handle_task_creation(user_message, user_data)
        
        elif any(word in message_lower for word in ["help", "what can you do", "commands"]):
            response = self._handle_help_query()
        
        else:
            response = self._handle_general_query(user_message, user_data)
        
        # Store response
        self.conversation_history.append({
            "assistant": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def _handle_recommendation_query(self, message, user_data):
        """Handle task assignment recommendations"""
        try:
            df = load_employee_data("data/employees.json")
            
            # Check if asking for specific department
            departments = ["engineering", "marketing", "sales", "hr", "finance"]
            specified_dept = None
            for dept in departments:
                if dept in message.lower():
                    specified_dept = dept.capitalize()
                    break
            
            if specified_dept and user_data and user_data.get("role") == "manager":
                # Filter to manager's department
                dept_employees = df[df['department'] == specified_dept]
                recs = recommend_task_redistribution(dept_employees)
            else:
                recs = recommend_task_redistribution(df)
            
            if not recs or 'message' in recs[0]:
                return "✅ Great news! Your team's workload is currently well-balanced. No immediate task redistribution needed."
            
            response = "📊 **AI Recommendations for Task Redistribution:**\n\n"
            
            for i, rec in enumerate(recs[:5], 1):  # Top 5 recommendations
                response += f"**{i}. {rec['priority']} Priority**\n"
                response += f"   • Move {rec['recommended_tasks_to_move']} tasks from **{rec['from_employee_name']}** "
                response += f"({rec['from_workload']} current tasks) to **{rec['to_employee_name']}** "
                response += f"(Capacity: {rec['to_capacity']})\n"
                response += f"   • Match Score: {rec['match_score']}\n"
                response += f"   • Reason: {rec['reason']}\n\n"
            
            return response
        
        except Exception as e:
            return f"⚠️ I encountered an error while analyzing recommendations: {str(e)}"
    
    def _handle_overload_query(self, user_data):
        """Handle queries about overloaded employees"""
        try:
            df = load_employee_data("data/employees.json")
            
            overloaded = df[
                (df['availability'] == 'Overloaded') | 
                (df['stress_indicators'].apply(lambda x: x['workload_rating']) > 7)
            ]
            
            if overloaded.empty:
                return "✅ Good news! No employees are currently overloaded."
            
            response = f"⚠️ **{len(overloaded)} Employee(s) Overloaded:**\n\n"
            
            for idx, emp in overloaded.iterrows():
                response += f"• **{emp['name']}** ({emp['department']})\n"
                response += f"  - Current Tasks: {emp['current_tasks']}\n"
                response += f"  - Hours/Week: {emp['hours_per_week']}\n"
                response += f"  - Stress Level: {emp['stress_indicators']['workload_rating']}/10\n"
                response += f"  - Missed Deadlines: {emp['stress_indicators']['missed_deadlines']}\n\n"
            
            response += "\n💡 **Suggestion:** Use the 'Recommend' button to get AI-powered task redistribution suggestions."
            
            return response
        
        except Exception as e:
            return f"⚠️ Error analyzing workload: {str(e)}"
    
    def _handle_availability_query(self, user_data):
        """Handle queries about available employees"""
        try:
            df = load_employee_data("data/employees.json")
            
            available = df[
                (df['availability'] == 'Available') & 
                (df['current_tasks'] < 10)
            ]
            
            if available.empty:
                return "⚠️ All employees are currently at capacity or overloaded."
            
            response = f"✅ **{len(available)} Employee(s) Available for New Tasks:**\n\n"
            
            for idx, emp in available.head(10).iterrows():
                capacity = ((15 - emp['current_tasks']) / 15) * 100
                response += f"• **{emp['name']}** ({emp['department']} - {emp['role']})\n"
                response += f"  - Current Tasks: {emp['current_tasks']}/15\n"
                response += f"  - Skill Level: {emp['skill_level']}/10\n"
                response += f"  - Capacity: {capacity:.0f}%\n"
                response += f"  - Completion Rate: {emp['completion_rate']*100:.0f}%\n\n"
            
            return response
        
        except Exception as e:
            return f"⚠️ Error finding available employees: {str(e)}"
    
    def _handle_balance_query(self, user_data):
        """Handle workload balancing queries"""
        return self._handle_recommendation_query("balance workload", user_data)
    
    def _handle_status_query(self, user_data):
        """Handle status and reporting queries"""
        try:
            df = load_employee_data("data/employees.json")
            
            total_employees = len(df)
            avg_tasks = df['current_tasks'].mean()
            avg_hours = df['hours_per_week'].mean()
            overloaded = len(df[df['availability'] == 'Overloaded'])
            available = len(df[df['availability'] == 'Available'])
            
            response = "📈 **Team Workload Status Report**\n\n"
            response += f"👥 Total Employees: {total_employees}\n"
            response += f"📊 Average Tasks per Employee: {avg_tasks:.1f}\n"
            response += f"⏰ Average Hours per Week: {avg_hours:.1f}\n"
            response += f"🔴 Overloaded: {overloaded} ({overloaded/total_employees*100:.1f}%)\n"
            response += f"🟢 Available: {available} ({available/total_employees*100:.1f}%)\n"
            response += f"🟡 Normal Load: {total_employees - overloaded - available}\n\n"
            
            if overloaded > total_employees * 0.3:
                response += "⚠️ **Alert:** More than 30% of employees are overloaded. Immediate action recommended!"
            elif overloaded > 0:
                response += "💡 **Tip:** Consider redistributing tasks to balance workload."
            else:
                response += "✅ **Status:** Team workload is healthy!"
            
            return response
        
        except Exception as e:
            return f"⚠️ Error generating status report: {str(e)}"
    
    def _handle_task_creation(self, message, user_data):
        """Handle task creation queries"""
        return "To create a new task, please use the 'Create New Task' section in the Manager Dashboard. I can help you find the best employee to assign it to!"
    
    def _handle_help_query(self):
        """Handle help queries"""
        return """🤖 **AI Assistant - Available Commands:**

📊 **Analytics:**
• "Show me overloaded employees"
• "Who is available for new tasks?"
• "Give me a status report"

🎯 **Recommendations:**
• "Recommend task redistribution"
• "Who should I assign this task to?"
• "Help me balance the workload"

📝 **Task Management:**
• "Create a new task" (via dashboard)
• "Show tasks for [employee name]"

💡 **Tips:**
• Be specific about departments (e.g., "Engineering team status")
• Ask about capacity and availability
• Get AI-powered assignment suggestions

**Just type your question naturally, and I'll help you manage your team's workload efficiently!** 🚀
"""
    
    def _handle_general_query(self, message, user_data):
        """Handle general queries"""
        return """I'm your AI Workload Management Assistant! 🤖

I can help you with:
• Task recommendations and assignments
• Finding overloaded or available employees
• Workload balancing and redistribution
• Team status and reports

Try asking:
• "Who is overloaded?"
• "Recommend task assignments"
• "Show team status"
• "Who can take a new task?"

Type 'help' for more commands!
"""

# Global chatbot instance
chatbot = WorkloadAIChatbot()

def get_chatbot_response(message, user_data=None):
    """Get response from chatbot"""
    return chatbot.process_message(message, user_data)
