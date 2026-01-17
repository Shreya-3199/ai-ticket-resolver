import uvicorn
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from duckduckgo_search import DDGS

# -------------------- Logging Setup --------------------
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------- FastAPI App --------------------
app = FastAPI(
    title="AI Ticket Resolution System",
    description="Offline AI-based classification with Online Web Search",
    version="1.4"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Data Models --------------------
class TicketRequest(BaseModel):
    title: str
    description: str

class TicketResponse(BaseModel):
    category: str
    priority: str
    resolution: str
    timestamp: str

# -------------------- Helper: Web Search (Smart Fallback) --------------------
def get_web_solutions(query: str):
    """Searches web. If API fails/finds nothing, returns a direct Google Search link."""
    results = []
    search_query = f"how to fix {query}"
    
    try:
        # Attempt 1: Try DuckDuckGo API
        with DDGS() as ddgs:
            # Region 'wt-wt' (World) helps avoid some IP blocks
            search_gen = ddgs.text(search_query, region='wt-wt', max_results=3)
            for r in search_gen:
                results.append(r['href'])

    except Exception as e:
        logging.error(f"Web Search API failed: {e}")

    # --- FALLBACK LOGIC ---
    # If the API found nothing (or failed), generate a manual link
    if not results:
        # Create a manual Google Search URL
        manual_link = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        return (
            f"\n\n🌍 **Web Search Recommendations:**\n"
            f"- {manual_link}"
        )

    # If API worked, return the specific links
    formatted_links = "\n".join([f"- {link}" for link in results])
    return f"\n\n🌍 **Web Search Recommendations:**\n{formatted_links}"

# -------------------- Rule-Based AI Logic --------------------
def analyze_ticket(ticket_title: str, ticket_desc: str):
    text = (ticket_title + " " + ticket_desc).lower()

    # Keyword lists
    auth_words = ["login", "password", "authentication", "auth", "sign-in"]
    server_words = ["server", "500", "crash", "down", "timeout"]
    perf_words = ["slow", "performance", "lag", "latency"]
    install_words = ["install", "setup", "config", "configuration"]
    net_words = ["network", "internet", "wifi", "connection", "dns"]

    # 1. Determine Category & Priority
    if any(word in text for word in auth_words):
        category = "Authentication Issue"
        priority = "High"
        base_resolution = "Ask user to reset password, verify credentials, and check authentication services."
        
    elif any(word in text for word in server_words):
        category = "Server Issue"
        priority = "Critical"
        base_resolution = "Check server logs, restart services, and alert the backend team immediately."
        
    elif any(word in text for word in perf_words):
        category = "Performance Issue"
        priority = "Medium"
        base_resolution = "Analyze system load, optimize database queries, and scale resources."
        
    elif any(word in text for word in install_words):
        category = "Installation Issue"
        priority = "Low"
        base_resolution = "Send installation documentation and verify system requirements."
        
    elif any(word in text for word in net_words):
        category = "Network Issue"
        priority = "High"
        base_resolution = "Check firewall rules, DNS settings, and general connectivity."
        
    else:
        category = "General Support"
        priority = "Low"
        base_resolution = "Request more details from the user and assign to a support agent."

    # 2. Fetch Web Results
    search_text = f"{ticket_title} {category}"
    web_links = get_web_solutions(search_text)

    # 3. Combine
    final_resolution = base_resolution + web_links

    return category, priority, final_resolution

# -------------------- API Endpoints --------------------
@app.post("/analyze-ticket", response_model=TicketResponse)
def analyze_ticket_api(ticket: TicketRequest):
    try:
        category, priority, resolution = analyze_ticket(ticket.title, ticket.description)

        logging.info(f"Analyzed Ticket: '{ticket.title}' -> {category}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return TicketResponse(
            category=category, 
            priority=priority, 
            resolution=resolution,
            timestamp=timestamp
        )

    except Exception as e:
        logging.error(f"Error analyzing ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
def root():
    return {"message": "AI Ticket Resolution System (Online v1.4) is running 🚀"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)