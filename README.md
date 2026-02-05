# SQL AI Agent - Customer Orders Analysis

An intelligent SQL agent that converts natural language questions into SQL queries, executes them against your customer order data, and explains the results in plain English.

Built with **Chainlit** and **Claude AI** (Anthropic).

## Quick Start

### Option 1: Upload CSV Directly in Chat (Easiest)

1. Setup environment and install dependencies (steps 1-3 below)
2. Configure your API key (step 4 below)
3. Run the application: `chainlit run app.py -w`
4. Drag & drop your CSV file into the chat window
5. The agent will convert it to a database automatically!

### Option 2: Use Setup Script

Follow the traditional setup process below and use `python setup_database.py`

---

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

### 4. Run the Application

```bash
chainlit run app.py -w
```

The app will open in your browser at `http://localhost:8000`

### 5. Upload Your Data

**Option A: Upload CSV in Chat (Recommended)**

1. Simply drag & drop your CSV file into the chat window
2. The agent will automatically:
   - Validate the file size (max 50 MB)
   - Convert it to a SQLite database
   - Display database statistics
   - Provide example questions to get started

**File Requirements:**
- **Format**: CSV files (`.csv`)
- **Size**: Maximum 50 MB
- **Structure**: Must include column headers in the first row
- **Encoding**: UTF-8 recommended

**Sample CSV Structure:**
```csv
order_id,product,quantity,price,customer,state,payment_method,order_date
1,Product A,10,100.00,Customer 1,California,Credit Card,2024-01-15
2,Product B,20,200.00,Customer 2,Texas,PayPal,2024-01-16
```

See `sample_template.csv` for a complete example.

**Option B: Use Setup Script**

1. Place your `customer_orders.csv` file in the project directory
2. Run: `python setup_database.py`

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

- 📁 **Enhanced CSV Upload**: 
  - Drag & drop CSV files directly in chat
  - Automatic file size validation (50 MB limit)
  - Detailed upload feedback with file statistics
  - Instant database conversion
  - Helpful error messages and troubleshooting tips
- 🤖 **Natural Language to SQL**: Convert questions directly into SQL queries
- 📊 **Automatic Query Execution**: Run queries against your data instantly
- 💡 **Plain English Explanations**: Get business-friendly insights, not raw data
- ✅ **Safety**: SQL query validation blocks dangerous operations
- 🔒 **Read-only Queries**: SELECT queries only (no modifications allowed)
- 📈 **Business Insights**: AI-powered analysis and recommendations

## Troubleshooting

**File Upload Issues:**

- **File too large**: 
  - Maximum file size is 50 MB
  - Try filtering your data to recent records only
  - Remove unnecessary columns
  - Split large files into smaller chunks

- **Invalid file format**:
  - Only CSV files (`.csv`) are supported
  - Ensure the file has a `.csv` extension
  - Check that the file is properly formatted with comma separators

- **Empty or corrupted file**:
  - Verify the CSV file contains data
  - Ensure column headers are present in the first row
  - Check for proper CSV formatting (no missing delimiters)
  - Try opening the file in a spreadsheet application to verify

**Database not found:**

- Run `python setup_database.py` first
- Or upload a CSV file directly in the chat
- Ensure `customer_orders.csv` exists if using setup script

**API Key errors:**

- Check `.env` file exists
- Verify API key is correct
- Ensure virtual environment is activated

**Import errors:**

- Verify all packages installed: `pip list`
- Reinstall if needed: `pip install -r requirements.txt`

## Running Tests

To run the test suite:

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_file_upload.py -v
```

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
