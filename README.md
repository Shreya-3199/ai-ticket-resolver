# AI Ticket Resolver 

## Overview
AI Ticket Resolver is a web-based system that classifies support tickets and provides suggested resolutions using **rule-based AI** and **online web search**.  
It helps users and support agents quickly identify ticket categories, priority levels, and possible solutions.

---

## Features
- **Ticket Classification**: Automatically categorizes tickets into Authentication, Server, Network, Performance, Installation, or General Support.  
- **Priority Detection**: Assigns Critical, High, Medium, or Low priority based on ticket content.  
- **Suggested Resolution**: Provides actionable steps to resolve issues and web resources for guidance.  
- **Dynamic Frontend**: Displays results with badges, clickable links, and timestamps.  

---

## Folder Structure
ai-ticket-resolver/
├─ index.html # Frontend HTML
├─ main.py # FastAPI backend
├─ requirements.txt # Python dependencies
├─ README.md # Project documentation
├─ AGILE.md # Agile documentation
├─ LICENSE # MIT License
Run Backend
python main.py


FastAPI server will start at http://127.0.0.1:8000

3. Open Frontend

Open index.html in your browser

Enter ticket title and description, then click Analyze Ticket

Ensure the backend is running for the frontend to fetch ticket analysis.

How It Works

Input: User enters a ticket title and description.

Processing: Backend uses rule-based logic to determine category, priority, and base resolution.

Web Search: Integrates DuckDuckGo search results to provide additional guidance.


Output: Frontend displays category, priority (badge), suggested resolution (with clickable links), and timestamp.
