import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from tools.mongodb_tool import MongoDBTool


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0.7
)


mongo = MongoDBTool()



@tool("Get Total Revenue")
def get_total_revenue() -> str:
    """Fetch total revenue from all completed payments."""
    try:
        return str(mongo.get_total_revenue())
    except Exception as e:
        return f"Error calculating total revenue: {str(e)}"

@tool("Get Outstanding Payments")
def get_outstanding_payments() -> str:
    """Calculate all unpaid/pending order totals."""
    try:
        return str(mongo.get_outstanding_payments())
    except Exception as e:
        return f"Error retrieving outstanding payments: {str(e)}"

@tool("Count Active vs Inactive Clients")
def count_active_inactive_clients() -> str:
    """Count number of active and inactive clients."""
    try:
        return str(mongo.count_active_inactive_clients())
    except Exception as e:
        return f"Error counting clients: {str(e)}"

@tool("Get New Clients This Month")
def get_new_clients_this_month() -> str:
    """Count new client registrations for the current month."""
    try:
        return str(mongo.get_new_clients_this_month())
    except Exception as e:
        return f"Error retrieving new clients: {str(e)}"

@tool("Get Enrollment Trends")
def get_enrollment_trends() -> str:
    """Analyze most enrolled courses/classes."""
    try:
        return str(mongo.get_enrollment_trends())
    except Exception as e:
        return f"Error retrieving enrollment trends: {str(e)}"

@tool("Get Top Services")
def get_top_services() -> str:
    """List top 5 services by revenue."""
    try:
        return str(mongo.get_top_services())
    except Exception as e:
        return f"Error retrieving top services: {str(e)}"

@tool("Get Course Completion Rates")
def get_course_completion_rates() -> str:
    """Fetch course counts grouped by completion status."""
    try:
        return str(mongo.get_course_completion_rates())
    except Exception as e:
        return f"Error retrieving completion rates: {str(e)}"

@tool("Get Attendance Percentage")
def get_attendance_percentage(class_name: str) -> str:
    """Return attendance % for a specific class name."""
    try:
        return str(mongo.get_attendance_percentage(class_name))
    except Exception as e:
        return f"Error calculating attendance percentage: {str(e)}"


dashboard_tools = [
    get_total_revenue,
    get_outstanding_payments,
    count_active_inactive_clients,
    get_new_clients_this_month,
    get_enrollment_trends,
    get_top_services,
    get_course_completion_rates,
    get_attendance_percentage
]


dashboard_agent = Agent(
    role="Business Analytics Agent",
    goal="Provide analytics and metrics useful for business owners",
    backstory="Business intelligence expert for fitness studio analytics.",
    tools=dashboard_tools,
    llm=llm,
    verbose=True,
    max_iter=3,
    allow_delegation=False
)

#task builder
def create_dashboard_task(prompt: str):
    return Task(
        description=f"""
        User Query: {prompt}

        Instructions:
        - Analyze the business-related query
        - Use tools to generate metrics/analytics
        - Format response clearly and helpfully
        - Keep it data-driven, professional, and insightful
        """,
        expected_output="A clear business insight or metric-driven answer",
        agent=dashboard_agent
    )

#crew builder
def get_dashboard_crew(prompt: str):
    try:
        task = create_dashboard_task(prompt)
        return Crew(
            agents=[dashboard_agent],
            tasks=[task],
            verbose=True,
            memory=False
        )
    except Exception as e:
        print(f"Error creating dashboard crew: {e}")
        raise

