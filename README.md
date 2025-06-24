# Multi-Agent Fitness Studio Management System

An AI-powered backend system for a fitness studio that leverages CrewAI agents to handle client support and business analytics queries through natural language. The project is built with FastAPI, MongoDB, and Streamlit, and utilizes structured tools for efficient data retrieval and order/enquiry management.

## Features

### **Agents**
- **Support Agent**: Handles service-related queries like course/class details, order/payment status, and client enquiries.
- **Dashboard Agent**: Provides business analytics and performance metrics

### **Tools**
- **MongoDB Tool**: Database operations for clients, orders, payments, and analytics
- **External API Tool**: Client registration and order creation
- **Memory Backend**: Session-based conversation memory
- **Translation Support**: Multi-language query handling


## Architecture

```
multi-agent/
├── agents/                # AI Agent definitions
│   ├── support_agent.py   # Customer support specialist
│   └── dashboard_agent.py # Business analytics expert
├── tools/                 # Tool implementations
│   ├── mongodb_tool.py    # Database operations
│   ├── external_api_tool.py # External integrations
│   └── memory_backend.py  # Conversation memory
├── models/                # Data models and schemas
│   ├── database.py        # MongoDB connection
│   └── schemas.py         # Pydantic models
├── apis/                  # API handlers
│   └── handlers.py        # FastAPI route handlers (for testing the tool routes)
├── data/                  # Mock data and seeding
│   ├── mock_data.py       # Test data generation
│   └── seed_database.py   # Database initialization
├── utils/                 # Utility functions
│   └── translate.py       # Language translation
├── main.py               # FastAPI application (backend)
└── app.py                # Streamlit frontend
```



## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- Google API Key (for Gemini LLM)

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd multi-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=fitness_studio
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Initialize Database

```bash
python data/seed_database.py
```

### 4. Start the Backend

```bash
uvicorn main:app --reload --port 8000
```

### 5. Launch Frontend (Optional)

```bash
streamlit run app.py
```

## Agent Capabilities

### Support Agent
**Role**: Fitness Studio Support Specialist
**Specializes in**:
- Client search and management
- Order tracking and status updates
- Payment inquiry handling
- Class scheduling and enrollment
- Service bookings and cancellations

**Available Tools**:
- `search_clients()` - Find clients by name, email, or phone
- `get_orders_by_client()` - Retrieve client order history
- `calculate_pending_dues()` - Check outstanding payments
- `list_upcoming_classes()` - Show scheduled classes
- `create_client_enquiry()` - Register new client
- `create_order()` - Place service orders

### Dashboard Agent
**Role**: Business Analytics Expert
**Specializes in**:
- Revenue analysis and reporting
- Client engagement metrics
- Service performance tracking
- Attendance monitoring
- Business intelligence insights

**Available Tools**:
- `get_total_revenue()` - Calculate total earnings
- `get_outstanding_payments()` - Pending payment analysis
- `count_active_inactive_clients()` - Client status overview
- `get_enrollment_trends()` - Popular services analysis
- `get_top_services()` - Revenue-generating services
- `get_attendance_percentage()` - Class attendance rates

## Database Schema

### Core Collections

#### Clients
#### Courses
#### Classes
#### Attendance
#### Orders
#### Payments


## API Endpoints

### Agent Queries (You can test using Postman)
```http
POST /support/query
Content-Type: application/json
{
    "prompt": "Show me all pending orders for John Wells"
}
```

```http
POST /dashboard/query  
Content-Type: application/json
{
    "prompt": "What's our total revenue this month?"
}
```

### Test Endpoints (Using Postman)
- `GET /test/..` for tool testing routes

## Query Examples

### Support Agent Queries

```bash
# Client Management
"Find all clients named Danielle"
"Show me orders for CLIENT_0001"
"What are the pending dues for Scott Brown?"

# Class Management
"Book CLIENT_0001 for the morning yoga class"

# Order Management
"Check the status of ORDER_00015"
"Show all cancelled orders this month"
"Create a new order for advanced pilates"
```

### Dashboard Agent Queries

```bash
# Revenue Analytics
"What's our total revenue?"
"Show outstanding payments summary"
"Which services generate the most revenue?"

# Client Analytics
"How many active clients do we have?"
"Show new client registrations this month"

# Performance Metrics
"What's the attendance rate for HIIT classes?"
"Show course completion statistics"
"Which instructor has the highest class attendance?"
```

## Memory & Context

The system maintains conversation context using MongoDB-backed memory:

```python
# Session-based memory
crew = get_support_crew(prompt, session_id="user_123")

# Automatic context retention
"Remember my previous question about John Doe"
"Continue with that client's order history"
```

## Multi-language Support

Built-in translation for non-English queries:

```python
# Automatic translation
"मुझे योग कक्षाओं की जानकारी चाहिए"  # Hindi
"Mostrar clases de pilates disponibles"   # Spanish
"Afficher le chiffre d'affaires total"    # French
```

### Sample Test Data
The system includes 50+ mock clients, 25 classes, 10 courses, and 100+ orders for comprehensive testing.

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017/` |
| `DATABASE_NAME` | Database name | `fitness_studio` |
| `GOOGLE_API_KEY` | Google Gemini API key | Required |

### Agent Configuration
```python
# Customize agent behavior
llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.7,  
    max_tokens=1000
)
```

