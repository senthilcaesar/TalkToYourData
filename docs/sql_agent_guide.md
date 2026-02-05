# SQL AI Agent with Chainlit - Complete Implementation Guide

## Project Overview
Build an AI-powered SQL agent that converts natural language questions into SQL queries, executes them against your customer order data, and explains results in plain English.

## Prerequisites
- Python 3.8 or higher
- Basic understanding of Python
- Anthropic API key (get one at https://console.anthropic.com)

## Step 1: Project Setup

### 1.1 Create Project Directory
```bash
mkdir sql-ai-agent
cd sql-ai-agent
```

### 1.2 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 1.3 Install Required Packages
```bash
pip install chainlit anthropic pandas sqlalchemy python-dotenv
```

### 1.4 Create Environment File
Create a file named `.env` in your project root:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Step 2: Prepare Your Data

### 2.1 Place Your CSV File
Put your customer orders CSV file in the project directory and name it `customer_orders.csv`

### 2.2 Create Database Setup Script
We'll convert the CSV to SQLite for easier querying.

Create `setup_database.py`:
```python
import pandas as pd
import sqlite3

def setup_database():
    """Convert CSV to SQLite database"""
    # Read CSV file
    df = pd.read_csv('customer_orders.csv')
    
    # Create SQLite database
    conn = sqlite3.connect('orders.db')
    
    # Write data to SQLite table
    df.to_sql('orders', conn, if_exists='replace', index=False)
    
    print(f"Database created successfully!")
    print(f"Total records: {len(df)}")
    print(f"\nColumn names:")
    for col in df.columns:
        print(f"  - {col}")
    
    conn.close()

if __name__ == "__main__":
    setup_database()
```

Run this script:
```bash
python setup_database.py
```

## Step 3: Build the SQL AI Agent

### 3.1 Create Main Application File
Create `app.py`:

```python
import chainlit as cl
from anthropic import Anthropic
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Database connection
DB_PATH = "orders.db"

def get_table_schema():
    """Get the database schema for the AI"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get column information
    cursor.execute("PRAGMA table_info(orders)")
    columns = cursor.fetchall()
    
    schema = "Table: orders\nColumns:\n"
    for col in columns:
        schema += f"  - {col[1]} ({col[2]})\n"
    
    conn.close()
    return schema

def execute_sql(query: str):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

def generate_sql_query(user_question: str, schema: str):
    """Use Claude to generate SQL query from natural language"""
    
    prompt = f"""You are a SQL expert. Given the following database schema and a user question, 
generate a valid SQLite query to answer the question.

Database Schema:
{schema}

User Question: {user_question}

Important:
- Generate ONLY the SQL query, no explanations
- Use proper SQLite syntax
- The table name is 'orders'
- Return only SELECT statements
- Use appropriate aggregations, GROUP BY, ORDER BY as needed

SQL Query:"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    sql_query = message.content[0].text.strip()
    # Clean up the query (remove markdown code blocks if present)
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    return sql_query

def explain_results(user_question: str, sql_query: str, results_df: pd.DataFrame):
    """Use Claude to explain the results in plain English"""
    
    # Convert results to string representation
    results_str = results_df.to_string(index=False)
    
    prompt = f"""You are a business analyst. Explain the following SQL query results in plain English.

User's Question: {user_question}

SQL Query Used:
{sql_query}

Results:
{results_str}

Provide a clear, concise explanation of what the data shows. Include:
1. Direct answer to the user's question
2. Key insights from the data
3. Any notable patterns or trends

Keep the explanation business-friendly and easy to understand."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

@cl.on_chat_start
async def start():
    """Welcome message when chat starts"""
    await cl.Message(
        content="""# 🤖 SQL AI Agent - Customer Orders Analysis

Welcome! I can help you analyze your customer order data using natural language.

**Example Questions:**
- What are your top 5 best-selling products and their revenue contribution?
- Which states/regions are your strongest markets?
- What is your monthly sales trend and growth pattern?
- What's the average order value by payment method?
- Which products have the highest profit margins?

Just ask your question in plain English, and I'll query the database for you!
"""
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages"""
    
    user_question = message.content
    
    # Show processing message
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Step 1: Get database schema
        await msg.stream_token("🔍 Analyzing your question...\n\n")
        schema = get_table_schema()
        
        # Step 2: Generate SQL query
        await msg.stream_token("⚙️ Generating SQL query...\n\n")
        sql_query = generate_sql_query(user_question, schema)
        
        await msg.stream_token(f"**Generated SQL:**\n```sql\n{sql_query}\n```\n\n")
        
        # Step 3: Execute query
        await msg.stream_token("📊 Executing query...\n\n")
        results_df, error = execute_sql(sql_query)
        
        if error:
            await msg.stream_token(f"❌ Error executing query: {error}\n\n")
            await msg.stream_token("Let me try to rephrase the query...\n")
            # You could add retry logic here
            return
        
        # Step 4: Display results
        await msg.stream_token(f"**Query Results:** ({len(results_df)} rows)\n\n")
        
        # Format results as markdown table
        if len(results_df) > 0:
            table_md = results_df.to_markdown(index=False)
            await msg.stream_token(f"```\n{table_md}\n```\n\n")
        else:
            await msg.stream_token("No results found.\n\n")
        
        # Step 5: Explain results
        await msg.stream_token("💡 **Analysis:**\n\n")
        explanation = explain_results(user_question, sql_query, results_df)
        await msg.stream_token(explanation)
        
    except Exception as e:
        await msg.stream_token(f"\n\n❌ An error occurred: {str(e)}")
    
    await msg.update()
```

## Step 4: Run Your Application

### 4.1 Start the Chainlit App
```bash
chainlit run app.py -w
```

The `-w` flag enables auto-reload when you make changes.

### 4.2 Access the Application
Open your browser and go to: `http://localhost:8000`

## Step 5: Testing Your Agent

Try these example questions:

1. **Top Products:**
   - "What are the top 5 best-selling products by quantity?"
   - "Show me the top 10 products by revenue"

2. **Regional Analysis:**
   - "Which states have the highest total sales?"
   - "What's the revenue breakdown by state?"

3. **Time-based Analysis:**
   - "What's the monthly sales trend for 2024?"
   - "Show me sales by day of the week"

4. **Payment Analysis:**
   - "What's the distribution of payment methods?"
   - "Average order value by payment type"

## Step 6: Customization & Improvements

### 6.1 Add Data Validation
You can add checks to ensure generated SQL is safe:

```python
def validate_sql(query: str):
    """Basic SQL validation"""
    query_lower = query.lower()
    
    # Only allow SELECT statements
    if not query_lower.strip().startswith('select'):
        raise ValueError("Only SELECT queries are allowed")
    
    # Disallow dangerous keywords
    dangerous = ['drop', 'delete', 'insert', 'update', 'alter', 'create']
    for word in dangerous:
        if word in query_lower:
            raise ValueError(f"Query contains forbidden keyword: {word}")
    
    return True
```

### 6.2 Add Query History
Store successful queries for learning:

```python
# Add to app.py
query_history = []

@cl.on_message
async def main(message: cl.Message):
    # ... existing code ...
    
    # After successful query
    query_history.append({
        'question': user_question,
        'sql': sql_query,
        'timestamp': pd.Timestamp.now()
    })
```

### 6.3 Add Visualization
Install plotly and create charts:

```bash
pip install plotly
```

```python
import plotly.express as px

def create_chart(df, query_type):
    """Create visualization based on query type"""
    if 'revenue' in df.columns or 'total' in df.columns:
        # Create bar chart
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])
        return fig
```

## Step 7: Deployment (Optional)

### 7.1 For Local Sharing
```bash
chainlit run app.py --host 0.0.0.0 --port 8000
```

### 7.2 For Production
Consider deploying to:
- Hugging Face Spaces
- Railway
- Render
- AWS/GCP/Azure

## Troubleshooting

### Common Issues:

1. **API Key Not Found**
   - Ensure `.env` file is in the project root
   - Check that `ANTHROPIC_API_KEY` is set correctly

2. **Database Not Found**
   - Run `setup_database.py` first
   - Ensure `customer_orders.csv` exists

3. **SQL Errors**
   - Check column names match your CSV
   - Verify data types in the database

4. **Import Errors**
   - Ensure all packages are installed in the virtual environment
   - Run `pip list` to verify installations

## Next Steps

1. **Add authentication** for multi-user scenarios
2. **Implement caching** for repeated queries
3. **Add export functionality** (CSV, Excel downloads)
4. **Create a query library** of common business questions
5. **Add natural language filters** ("last 30 days", "top 10", etc.)

## Resources

- Chainlit Documentation: https://docs.chainlit.io
- Anthropic API Docs: https://docs.anthropic.com
- SQLite Tutorial: https://www.sqlitetutorial.net

## Support

If you encounter issues:
1. Check the console for error messages
2. Verify your API key is valid
3. Test SQL queries manually in SQLite browser
4. Review Chainlit logs for debugging

Happy coding! 🚀
