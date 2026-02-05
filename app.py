"""
SQL AI Agent - Google AI Studio Style
Powered by Chainlit and Claude AI
"""

import chainlit as cl
from anthropic import Anthropic
import sqlite3
import pandas as pd
import os
import shutil
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Database configuration
DB_PATH = "orders.db"

# File upload configuration
MAX_FILE_SIZE_MB = 50  # Maximum file size in MB
ACCEPTED_MIME_TYPES = ["text/csv", "application/vnd.ms-excel", "application/csv"]

def convert_csv_to_db(csv_file_path: str, output_db_path: str = None):
    """
    Convert a CSV file to SQLite database
    References the logic from setup_database.py
    """
    if output_db_path is None:
        output_db_path = DB_PATH
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        if len(df) == 0:
            return False, "CSV file is empty"
        
        # Create SQLite database
        conn = sqlite3.connect(output_db_path)
        
        # Write data to SQLite table (replace existing table)
        df.to_sql('orders', conn, if_exists='replace', index=False)
        
        # Verify the data
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return True, {
            'records': count,
            'columns': len(df.columns),
            'column_names': list(df.columns)
        }
        
    except Exception as e:
        return False, str(e)

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
        welcome_msg = """# TalkToYourData - Sales Insight Bot

## Getting Started

### Upload a CSV File
Use the **file upload button** (📎 paperclip icon) in the chat input below or drag & drop a CSV file. The AI agent will automatically convert it to a database!

**File Requirements:**
- Format: CSV files (`.csv`)
- Size: Maximum 50 MB
- Must include column headers

### Or Use the Setup Script
Run the setup script if you have a CSV file in your project directory:

```bash
python setup_database.py
```

---

## Once Your Database is Ready

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
"""
    else:
        welcome_msg = """# TalkToYourData - Sales Insight Bot

Ask questions about your customer orders in natural language. I'll analyze your data and provide insights. Your question is translated into SQL, run against your dataset, and the results are summarized in plain English.

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

"""
    
    await cl.Message(content=welcome_msg).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and process queries or file uploads"""
    
    # Check if user uploaded a file
    if message.elements:
        csv_files = [el for el in message.elements if el.mime in ACCEPTED_MIME_TYPES]
        
        if csv_files:
            for file_element in csv_files:
                msg = cl.Message(content="")
                await msg.send()
                
                try:
                    # Get file size in MB
                    file_size_mb = os.path.getsize(file_element.path) / (1024 * 1024)
                    
                    await msg.stream_token(f"📁 **Processing CSV file:** `{file_element.name}`\n\n")
                    await msg.stream_token(f"📏 **File size:** {file_size_mb:.2f} MB\n\n")
                    
                    # Validate file size
                    if file_size_mb > MAX_FILE_SIZE_MB:
                        await msg.stream_token(f"❌ **File too large!**\n\n")
                        await msg.stream_token(f"The uploaded file ({file_size_mb:.2f} MB) exceeds the maximum allowed size of {MAX_FILE_SIZE_MB} MB.\n\n")
                        await msg.stream_token(f"**Suggestions:**\n")
                        await msg.stream_token(f"- Try filtering your data to include only recent records\n")
                        await msg.stream_token(f"- Remove unnecessary columns\n")
                        await msg.stream_token(f"- Split the file into smaller chunks\n")
                        await msg.update()
                        return
                    
                    await msg.stream_token("⚙️ Converting CSV to database...\n\n")
                    
                    # Convert CSV to database
                    success, result = convert_csv_to_db(file_element.path)
                    
                    if success:
                        await msg.stream_token(f"✅ **Successfully converted to database!**\n\n")
                        await msg.stream_token(f"📊 **Database Statistics:**\n")
                        await msg.stream_token(f"- **File Name**: {file_element.name}\n")
                        await msg.stream_token(f"- **File Size**: {file_size_mb:.2f} MB\n")
                        await msg.stream_token(f"- **Total Records**: {result['records']:,}\n")
                        await msg.stream_token(f"- **Total Columns**: {result['columns']}\n")
                        await msg.stream_token(f"- **Column Names**: `{', '.join(result['column_names'])}`\n\n")
                        await msg.stream_token(f"💾 **Database Location**: `{DB_PATH}`\n\n")
                        await msg.stream_token("---\n\n")
                        await msg.stream_token("✨ **Ready to analyze!** You can now ask questions about your data.\n\n")
                        await msg.stream_token("**Try these example questions:**\n")
                        await msg.stream_token("- What are the top 5 products by revenue?\n")
                        await msg.stream_token("- Show me the sales trend by month\n")
                        await msg.stream_token("- Which region has the highest sales?\n")
                    else:
                        await msg.stream_token(f"❌ **Error converting CSV**\n\n")
                        await msg.stream_token(f"**Error details:**\n```\n{result}\n```\n\n")
                        await msg.stream_token(f"**Troubleshooting tips:**\n")
                        await msg.stream_token(f"- Ensure the CSV file is properly formatted\n")
                        await msg.stream_token(f"- Check that the file is not corrupted\n")
                        await msg.stream_token(f"- Verify that the file contains data (not empty)\n")
                        await msg.stream_token(f"- Make sure column headers are present\n")
                        
                except Exception as e:
                    await msg.stream_token(f"❌ **Unexpected Error**\n\n")
                    await msg.stream_token(f"```\n{str(e)}\n```\n\n")
                    await msg.stream_token(f"Please try again or contact support if the issue persists.\n")
                
                await msg.update()
            return
        else:
            # File uploaded but not CSV
            if message.elements:
                uploaded_file = message.elements[0]
                await cl.Message(
                    content=f"⚠️ **Invalid file type**\n\n"
                            f"You uploaded: `{uploaded_file.name}` (type: `{uploaded_file.mime}`)\n\n"
                            f"**Accepted formats:**\n"
                            f"- CSV files (`.csv`)\n"
                            f"- Maximum size: {MAX_FILE_SIZE_MB} MB\n\n"
                            f"Please upload a valid CSV file and try again.",
                    author="System"
                ).send()
                return
    
    # Normal chat flow - answer questions about the database
    user_question = message.content.strip() if message.content else ""
    
    # If there's no text content
    if not user_question:
        if not message.elements:
            await cl.Message(content="Please ask a question about your data or upload a CSV file.").send()
        return
    
    # Create a message to stream updates
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # First check if database exists
        if not os.path.exists(DB_PATH):
            await msg.stream_token("📁 **No database found yet.**\n\n")
            await msg.stream_token("Please upload a CSV file or run `python setup_database.py` first.\n")
            await msg.update()
            return
            
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
