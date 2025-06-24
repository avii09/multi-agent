import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from tools.mongodb_tool import MongoDBTool
from tools.external_api_tool import ExternalAPITool
from utils.translate import translate_to_english
from tools.memory_backend import MongoMemoryBackend

memory_backend = MongoMemoryBackend()

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")


llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0.7
)


mongo = MongoDBTool()
external = ExternalAPITool()


@tool("Search Clients")
def search_clients(query: str) -> str:
    """Search for clients by name, email, or phone."""
    try:
        result = mongo.search_clients(query)
        return str(result)
    except Exception as e:
        return f"Error searching for clients: {str(e)}"

@tool("Get Orders by Client")
def get_orders_by_client(client_id: str) -> str:
    """Get all orders for a client."""
    try:
        result = mongo.get_orders_by_client(client_id)
        return str(result)
    except Exception as e:
        return f"Error retrieving orders for client {client_id}: {str(e)}"

@tool("Get Order by ID")
def get_order_by_id(order_id: str) -> str:
    """Retrieve an order using the order ID."""
    try:
        result = mongo.get_order_by_id(order_id)
        return str(result)
    except Exception as e:
        return f"Error retrieving order {order_id}: {str(e)}"

@tool("Filter Orders by Status")
def filter_orders_by_status(status: str) -> str:
    """List orders by their payment status."""
    try:
        result = mongo.filter_orders_by_status(status)
        return str(result)
    except Exception as e:
        return f"Error filtering orders by status {status}: {str(e)}"

@tool("Get Payment Details")
def get_payment_details(order_id: str) -> str:
    """Fetch payment details for an order."""
    try:
        result = mongo.get_payment_details(order_id)
        return str(result)
    except Exception as e:
        return f"Error retrieving payment details for order {order_id}: {str(e)}"

@tool("Calculate Pending Dues")
def calculate_pending_dues(client_id: str) -> str:
    """Calculate how much a client owes."""
    try:
        result = mongo.calculate_pending_dues(client_id)
        return str(result)
    except Exception as e:
        return f"Error calculating pending dues for client {client_id}: {str(e)}"

@tool("List Upcoming Classes")
def list_upcoming_classes() -> str:
    """List upcoming scheduled classes."""
    try:
        result = mongo.list_upcoming_classes()
        return str(result)
    except Exception as e:
        return f"Error retrieving upcoming classes: {str(e)}"

@tool("Filter Classes by Instructor")
def filter_classes_by_instructor(instructor_name: str) -> str:
    """Find classes conducted by a specific instructor."""
    try:
        result = mongo.filter_classes_by_instructor(instructor_name)
        return str(result)
    except Exception as e:
        return f"Error retrieving classes for instructor {instructor_name}: {str(e)}"

@tool("Create Client Enquiry")
def create_client_enquiry(enquiry_data: str) -> str:
    """Register a new client enquiry."""
    try:
        result = external.create_client_enquiry(enquiry_data)
        return str(result)
    except Exception as e:
        return f"Error creating client enquiry: {str(e)}"

@tool("Create Order")
def create_order(order_data: str) -> str:
    """Place a new service order for a client."""
    try:
        result = external.create_order(order_data)
        return str(result)
    except Exception as e:
        return f"Error creating order: {str(e)}"


support_tools = [
    search_clients,
    get_orders_by_client,
    get_order_by_id,
    filter_orders_by_status,
    get_payment_details,
    calculate_pending_dues,
    list_upcoming_classes,
    filter_classes_by_instructor,
    create_client_enquiry,
    create_order
]


support_agent = Agent(
    role="Fitness Studio Support Specialist",
    goal="Provide excellent customer service by handling inquiries about classes, orders, payments, and bookings with accuracy and professionalism",
    backstory="""You are an experienced customer service specialist for a premium fitness studio. 
    You have deep knowledge of fitness programs, class schedules, payment systems, and client management. 
    You're known for being helpful, patient, and solution-oriented. You always strive to resolve 
    client issues efficiently while maintaining a friendly and professional demeanor.""",
    tools=support_tools,
    llm=llm,
    verbose=True,
    max_iter=3,
    allow_delegation=False
)

#task builder
def create_support_task(prompt: str):
    enhanced_description = f"""
    User Query: {prompt}

    Instructions:
    1. Analyze the user's request carefully
    2. Use appropriate tools to gather necessary information
    3. Provide a clear, helpful, and professional response
    4. If you encounter errors, explain them clearly and suggest alternatives
    5. Always be courteous and solution-oriented
    """
    return Task(
        description=enhanced_description,
        expected_output="""A comprehensive and helpful response that:
        - Directly addresses the user's question or request
        - Provides specific information when available
        - Offers clear next steps or alternatives if needed
        - Maintains a professional and friendly tone
        - Includes relevant details like order numbers, dates, or amounts when applicable""",
        agent=support_agent
    )

#crew builder
def get_support_crew(prompt: str, session_id: str = "default_user"):
    try:
        memory_log = memory_backend.get_memory(session_id)
        memory_context = "\n".join(memory_log)

        translated_prompt = translate_to_english(llm, prompt)
        full_prompt = f"{memory_context}\n\nNew Query: {translated_prompt}"

        memory_backend.save_memory(session_id, translated_prompt)

        task = create_support_task(full_prompt)
        return Crew(
            agents=[support_agent],
            tasks=[task],
            verbose=True,
            memory=True,
            max_rpm=10
        )
    except Exception as e:
        print(f"Error creating crew: {e}")
        raise
