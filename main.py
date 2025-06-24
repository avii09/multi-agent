from fastapi import FastAPI, Body, Header
from apis.handlers import router
from agents.support_agent import get_support_crew
from agents.dashboard_agent import get_dashboard_crew

app = FastAPI(title="Multi-Agent Backend API")

#test routes from apis.handlers
app.include_router(router)

@app.post("/support/query")
async def support_query(prompt: str = Body(..., embed=True), session_id: str = Header(default="default_user")):
    crew = get_support_crew(prompt, session_id=session_id)
    result = crew.kickoff()
    return {"response": result}

@app.post("/dashboard/query")
async def dashboard_query(prompt: str = Body(..., embed=True), session_id: str = Header(default="default_user")):
    crew = get_dashboard_crew(prompt, session_id=session_id)
    result = crew.kickoff()
    return {"response": result}
