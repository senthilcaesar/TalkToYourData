# SQL AI Agent - Customer Orders Analysis

An intelligent SQL agent that converts natural language questions into SQL queries, executes them against your customer order data, and explains the results in plain English.

Built with **Chainlit** and **Claude AI** (Anthropic).

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Get your Anthropic API key from: https://console.anthropic.com

3. Edit `.env` and add your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```

### 4. Prepare Your Data

1. Place your `customer_orders.csv` file in the project directory

2. Run the setup script to create the database:
   ```bash
   python setup_database.py
   ```

### 5. Run the Application

```bash
chainlit run app.py -w
```

The app will open in your browser at `http://localhost:8000`

## Example Questions

- What are the top 5 best-selling products by revenue?
- Which states are our strongest markets?
- What's the monthly sales trend for 2024?
- What's the average order value by payment method?
- Which products have the highest profit margins?

## Project Structure

```
sql-ai-agent/
├── app.py                  # Main Chainlit application
├── setup_database.py       # Database setup script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Example environment file
├── customer_orders.csv    # Your CSV data (add this)
└── orders.db              # SQLite database (created by setup)
```

## Features

- 🤖 Natural language to SQL conversion
- 📊 Automatic query execution
- 💡 Plain English explanations
- ✅ SQL query validation for safety
- 🔒 Read-only queries (SELECT only)
- 📈 Business insights generation

## Troubleshooting

**Database not found:**
- Run `python setup_database.py` first
- Ensure `customer_orders.csv` exists

**API Key errors:**
- Check `.env` file exists
- Verify API key is correct
- Ensure virtual environment is activated

**Import errors:**
- Verify all packages installed: `pip list`
- Reinstall if needed: `pip install -r requirements.txt`

## Technologies Used

- **Chainlit**: Chat UI framework
- **Claude AI**: Natural language processing
- **SQLite**: Embedded database
- **Pandas**: Data manipulation
- **Python**: Core programming language

## License

MIT License

## Support

For issues or questions, check the detailed guide in `sql_agent_guide.md`
