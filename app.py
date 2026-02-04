"""
SQL AI Agent - Google AI Studio Style
Powered by Chainlit and Claude AI
"""

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

# Database configuration
DB_PATH = "orders.db"

def get_table_schema():
    """Get the database schema to provide context to the AI"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get column information
    cursor.execute("PRAGMA table_info(orders)")
    columns = cursor.fetchall()
    
    # Get sample data for better context
    cursor.execute("SELECT * FROM orders LIMIT 3")
    sample_data = cursor.fetchall()
    
    schema = "Table: orders\n\nColumns:\n"
    for col in columns:
        schema += f"  - {col[1]} ({col[2]})\n"
    
    schema += "\nSample Data:\n"
    schema += str(sample_data[:2])  # Show 2 sample rows
    
    conn.close()
    return schema

def validate_sql(query: str):
    """Validate SQL query for safety"""
    query_lower = query.lower().strip()
    
    # Only allow SELECT statements
    if not query_lower.startswith('select'):
        raise ValueError("⚠️ Only SELECT queries are allowed for safety")
    
    # Disallow dangerous keywords
    dangerous_keywords = ['drop', 'delete', 'insert', 'update', 'alter', 'create', 'truncate']
    for keyword in dangerous_keywords:
        if keyword in query_lower:
            raise ValueError(f"⚠️ Query contains forbidden keyword: {keyword}")
    
    return True

def execute_sql(query: str):
    """Execute SQL query and return results as DataFrame"""
    try:
        # Validate query first
        validate_sql(query)
        
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

def generate_sql_query(user_question: str, schema: str):
    """Use Claude to generate SQL query from natural language"""
    
    prompt = f"""You are a SQL expert helping to analyze customer order data. 
Given the database schema and a user question, generate a valid SQLite query.

Database Schema:
{schema}

User Question: {user_question}

Instructions:
- Generate ONLY the SQL query, no explanations or markdown
- Use proper SQLite syntax
- The table name is 'orders'
- Return only SELECT statements
- Use appropriate aggregations (SUM, COUNT, AVG) as needed
- Use GROUP BY for aggregations
- Use ORDER BY to sort results meaningfully
- Limit results to top 10-20 items for large datasets
- Handle NULL values appropriately

SQL Query:"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    sql_query = message.content[0].text.strip()
    
    # Clean up the query (remove markdown code blocks if present)
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    # Remove any trailing semicolon (SQLite doesn't require it)
    sql_query = sql_query.rstrip(';')
    
    return sql_query

def explain_results(user_question: str, sql_query: str, results_df: pd.DataFrame):
    """Use Claude to explain the results in plain English"""
    
    # Prepare results summary
    if len(results_df) == 0:
        results_str = "No results found"
    else:
        # Convert to string, limit to first 20 rows for context
        results_str = results_df.head(20).to_string(index=False)
        if len(results_df) > 20:
            results_str += f"\n\n... and {len(results_df) - 20} more rows"
    
    prompt = f"""You are a business analyst explaining data insights to stakeholders.

User's Question: {user_question}

SQL Query Used:
{sql_query}

Query Results:
{results_str}

Provide a clear, business-friendly explanation that includes:
1. Direct answer to the question
2. Key insights and patterns in the data
3. Notable trends or outliers
4. Actionable recommendations if applicable

Keep the tone professional but conversational. Use numbers and percentages where relevant."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

@cl.on_chat_start
async def start():
    """Welcome message when chat starts - Google AI Studio style"""
    
    # Check if database exists
    if not os.path.exists(DB_PATH):
        await cl.Message(
            content="""# Database Not Found

Please run the setup script first:

```bash
python setup_database.py
```

Make sure your `customer_orders.csv` file is in the project directory.
"""
        ).send()
        return
    
    welcome_msg = """# TalkToYourData - Sales Insight Bot

Ask questions about your customer orders in natural language. I'll analyze your data and provide insights. Your question is translated into SQL, run against your dataset, and the results are summarized in plain English.

### Example Questions

**Sales Performance**
• What are the top 5 products by revenue?
• Show me monthly revenue trends

**Regional Analysis**
• Which states generate the most sales?
• What's the revenue distribution by region?

**Customer Insights**
• What's the average order value?
• Which payment methods are most popular?

**Product Analysis**
• Which products have the highest profit margins?
• What are our best-selling SKUs?

Just type your question below to get started.
"""
    
    await cl.Message(content=welcome_msg).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and process queries"""
    
    user_question = message.content
    
    # Create a message to stream updates
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Step 1: Analyze question
        await msg.stream_token("Analyzing your question...\n\n")
        schema = get_table_schema()
        
        # Step 2: Generate SQL query
        await msg.stream_token("Generating SQL query...\n\n")
        sql_query = generate_sql_query(user_question, schema)
        
        await msg.stream_token(f"**Generated Query**\n\n```sql\n{sql_query}\n```\n\n")
        
        # Step 3: Execute query
        await msg.stream_token("Executing query...\n\n")
        results_df, error = execute_sql(sql_query)
        
        if error:
            await msg.stream_token(f"**Error**\n\n```\n{error}\n```\n\n")
            await msg.stream_token("Please try rephrasing your question.")
            await msg.update()
            return
        
        # Step 4: Display results
        row_count = len(results_df)
        await msg.stream_token(f"**Results** • {row_count} row(s)\n\n")
        
        # Format and display results
        if row_count > 0:
            # Show results as a formatted table
            display_df = results_df.head(15)
            table_md = display_df.to_markdown(index=False)
            await msg.stream_token(f"{table_md}\n\n")
            
            if row_count > 15:
                await msg.stream_token(f"*Showing 15 of {row_count} rows*\n\n")
            
            # Step 5: Generate insights
            await msg.stream_token("---\n\n**Insights**\n\n")
            explanation = explain_results(user_question, sql_query, results_df)
            await msg.stream_token(explanation)
            
        else:
            await msg.stream_token("No results found. Try a different question.\n")
        
    except Exception as e:
        await msg.stream_token(f"\n\n**Error**\n\n```\n{str(e)}\n```\n\n")
        await msg.stream_token("Please try asking your question differently.")
    
    # Update the message
    await msg.update()

if __name__ == "__main__":
    # This is only used for local testing
    pass
