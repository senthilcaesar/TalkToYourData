# UI Enhancement Guide for SQL AI Agent

## Option 1: Customize Chainlit's Built-in UI (Easiest) ⭐ RECOMMENDED

Chainlit already has a beautiful UI that you can customize extensively!

### A. Custom Branding & Styling

Create `.chainlit/config.toml` (already created when you first ran the app):

```toml
[project]
# Enable public access
enable_telemetry = true

[UI]
# App name and description
name = "SQL Business Intelligence Agent"
description = "AI-powered analytics for your customer orders"

# Custom colors and theme
[UI.theme]
primary_color = "#2563eb"  # Blue
background_color = "#ffffff"
text_color = "#1f2937"

[UI.theme.dark]
primary_color = "#3b82f6"
background_color = "#111827"
text_color = "#f9fafb"

# Custom logo and favicon
[UI]
# Add your logo (place logo.png in .chainlit folder)
default_collapse_content = true
default_expand_messages = false
hide_cot = false

# GitHub link
github = "https://github.com/yourusername/sql-ai-agent"

[UI.footer]
# Custom footer text
name = "Built with ❤️ using Chainlit & Claude AI"
url = "https://yourcompany.com"
```

### B. Add Custom CSS

Create `.chainlit/custom.css`:

```css
/* Custom styling for your SQL AI Agent */

/* Main container */
#root {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Chat messages */
.message-content {
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* SQL code blocks - make them stand out */
.message-content pre {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    padding: 16px;
    color: white;
}

/* Tables - professional look */
.message-content table {
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.message-content th {
    background: #2563eb;
    color: white;
    font-weight: 600;
    padding: 12px 16px;
}

.message-content td {
    padding: 10px 16px;
    border-bottom: 1px solid #e5e7eb;
}

.message-content tr:hover {
    background: #f9fafb;
}

/* Input box */
#chat-input {
    border-radius: 24px;
    border: 2px solid #e5e7eb;
    padding: 12px 20px;
    font-size: 15px;
}

#chat-input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Send button */
button[type="submit"] {
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    width: 44px;
    height: 44px;
}

/* Welcome message card */
.step:first-child .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 32px;
    border-radius: 16px;
}

/* Status indicators */
.message-content strong {
    color: #2563eb;
}

/* Insights section */
.message-content hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    margin: 24px 0;
}
```

### C. Add Custom Logo and Favicon

1. Create a `.chainlit` folder (if not exists)
2. Add your images:
   - `logo_light.png` - Logo for light mode (200x50px recommended)
   - `logo_dark.png` - Logo for dark mode
   - `favicon.png` - Browser tab icon (32x32px)

---

## Option 2: Build Custom Web Dashboard with Streamlit

If you want more control, create a dashboard-style UI with Streamlit.

### Install Streamlit
```bash
pip install streamlit plotly
```

### Create `streamlit_app.py`:

```python
import streamlit as st
from anthropic import Anthropic
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()

# Page config
st.set_page_config(
    page_title="SQL Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
DB_PATH = "orders.db"

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x50/667eea/ffffff?text=Your+Logo", use_container_width=True)
    st.title("🤖 SQL AI Agent")
    st.markdown("---")
    
    # Quick stats
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        total_orders = pd.read_sql_query("SELECT COUNT(*) as cnt FROM orders", conn).iloc[0]['cnt']
        total_revenue = pd.read_sql_query("SELECT SUM(`Invoice Value`) as total FROM orders", conn).iloc[0]['total']
        conn.close()
        
        st.metric("Total Orders", f"{total_orders:,}")
        st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    
    st.markdown("---")
    st.markdown("### 📌 Quick Actions")
    quick_questions = [
        "Top 5 products by revenue",
        "Sales by state",
        "Monthly trends",
        "Best selling SKUs",
        "Profit margins"
    ]
    
    for q in quick_questions:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.query = q

# Main content
st.markdown('<h1 class="main-header">📊 Business Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown("Ask questions about your customer orders in plain English")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Ask Questions", "📈 Analytics", "📋 Raw Data"])

with tab1:
    # Query input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Your Question",
            value=st.session_state.get('query', ''),
            placeholder="e.g., What are my top 5 products by revenue?",
            label_visibility="collapsed"
        )
    
    with col2:
        analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_btn and query:
        with st.spinner("🤖 AI is analyzing your question..."):
            # Your existing logic here
            st.success("Analysis complete!")
            
            # Display SQL
            with st.expander("📝 Generated SQL Query", expanded=True):
                st.code("SELECT * FROM orders LIMIT 10", language="sql")
            
            # Display results
            st.markdown("### 📊 Results")
            # Your results table here
            
            # Display insights
            st.markdown("### 💡 Insights")
            st.info("Your AI-generated insights here...")

with tab2:
    st.markdown("### 📈 Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue Over Time")
        # Add your chart here
        
    with col2:
        st.markdown("#### Top Products")
        # Add your chart here

with tab3:
    st.markdown("### 📋 Database Preview")
    
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM orders LIMIT 100", conn)
        conn.close()
        
        st.dataframe(df, use_container_width=True, height=500)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Claude AI & Python")
```

### Run Streamlit App:
```bash
streamlit run streamlit_app.py
```

---

## Option 3: Modern React Dashboard (Most Professional)

Build a full-featured web app with React + FastAPI backend.

### Backend API (`api.py`):

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SQL AI Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
DB_PATH = "orders.db"

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    results: list
    explanation: str
    status: str

@app.post("/api/query", response_model=QueryResponse)
async def query_data(request: QueryRequest):
    """Process natural language query"""
    try:
        # Your existing logic here
        return QueryResponse(
            sql="SELECT * FROM orders",
            results=[],
            explanation="Your explanation",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get database statistics"""
    conn = sqlite3.connect(DB_PATH)
    # Return stats
    conn.close()
    return {"total_orders": 1000, "total_revenue": 50000}
```

### Frontend (React - Basic structure):

```bash
npx create-react-app sql-ai-frontend
cd sql-ai-frontend
npm install axios recharts tailwindcss
```

---

## Option 4: No-Code Solutions

### A. Integrate with Retool
- Connect your database
- Build custom dashboards
- Add AI chat widget

### B. Use Bubble.io
- Visual development
- Connect via API
- Professional templates

---

## RECOMMENDATION 🌟

**For your use case, I recommend:**

1. **Start with Chainlit customization** (Option 1) - You already have it running!
   - Customize the config.toml
   - Add custom CSS
   - Add your logo
   - Takes 15 minutes, looks professional

2. **Add Streamlit dashboard** (Option 2) for analytics view
   - Great for executives
   - Easy to add charts
   - Can run alongside Chainlit

3. **Later, build React app** (Option 3) for production
   - Most professional
   - Full control
   - Best for client-facing

---

## Next Steps

1. Customize Chainlit config (easiest win)
2. Add custom CSS for branding
3. Try Streamlit for dashboard view
4. Let me know which option you'd like me to build out fully!

Would you like me to create the complete customized Chainlit UI for you, or build a full Streamlit dashboard?
