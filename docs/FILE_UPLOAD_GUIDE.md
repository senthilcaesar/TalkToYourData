# CSV File Upload Guide

## How to Upload CSV Files

The **TalkToYourData** SQL AI Agent now supports direct CSV file uploads through the chat interface!

### Direct Upload Method (Recommended)

1. **Open the Chat Interface**
   - Run: `chainlit run app.py -w`
   - The application will open in your browser at `http://localhost:8000`

2. **Upload Your CSV**
   - Look for the **paperclip icon** or **upload button** in the chat input area
   - Click it to select a CSV file from your computer
   - Alternatively, you can **drag and drop** a CSV file into the chat window

3. **Automatic Processing**
   - The AI Agent will:
     - Detect and validate the CSV file
     - Parse all columns and data
     - Create a SQLite database automatically
     - Return database statistics

4. **Start Asking Questions**
   - Once uploaded, you can immediately ask questions about your data
   - Example: "What are the top 5 products by revenue?"

### What Gets Uploaded

- **File Type**: CSV (Comma-Separated Values)
- **Size**: Up to 50MB
- **Format**: Any CSV structure is supported
- **Columns**: Automatically detected and preserved
- **Data Types**: Automatically inferred from the data

### What Happens Behind the Scenes

```
CSV File → Uploaded → Parsed → SQLite Database → Ready for Queries
                ↓
        Stats Returned to User
```

1. **File Upload**: Your CSV file is uploaded to the chat
2. **Parsing**: The file is parsed using pandas
3. **Database Creation**: An SQLite database is created from the CSV
4. **Validation**: Data is verified and row count is confirmed
5. **Ready**: Database is immediately ready for natural language queries

### Database Statistics

After uploading, you'll see:

- ✅ Number of records imported
- 📊 Number of columns detected
- 📋 Column names for reference
- 💾 Database file location

### Example Upload Scenarios

**Scenario 1: Customer Orders**

- Upload: `customer_orders.csv`
- Get: Instant database with order data
- Ask: "Which customers made the most purchases?"

**Scenario 2: Sales Data**

- Upload: `sales_2024.csv`
- Get: Database with sales information
- Ask: "What's the top region by revenue?"

**Scenario 3: Product Catalog**

- Upload: `products.csv`
- Get: Product database
- Ask: "Which products have the highest profit margins?"

### Troubleshooting

**Q: The upload button doesn't appear**

- Ensure you're using Chainlit 2.0 or later
- Refresh the browser page
- Check browser console for errors

**Q: "File is not a CSV" error**

- Ensure your file has a `.csv` extension
- Verify the file is in CSV format (not Excel, JSON, etc.)
- Try opening it in a text editor to confirm format

**Q: Database conversion fails**

- Check that the CSV file is valid and not corrupted
- Ensure all rows have the same number of columns
- Try uploading a smaller subset of your data first

**Q: Can't find the upload button**

- Look for the 📎 (paperclip) icon in the chat input area
- Some browsers may require clicking the attachment icon first
- Try dragging and dropping the file directly into the chat

### Alternative: Command Line Setup

If you prefer not to use the chat interface upload:

```bash
# Place your CSV in the project directory
cp /path/to/your/data.csv customer_orders.csv

# Run the setup script
python setup_database.py

# Start the app
chainlit run app.py -w
```

### Supported CSV Structures

The upload feature works with ANY CSV structure, including:

- ✅ Headers on first row
- ✅ Multiple column types (numeric, text, dates)
- ✅ Missing values / NULL data
- ✅ Unicode and special characters
- ✅ Large datasets (50MB+)
- ✅ Any number of columns

### After Upload: Query Examples

Once your CSV is converted to a database, you can ask:

**Data Exploration**

- "Show me the first few rows"
- "What columns are in this data?"
- "How many records total?"

**Analysis**

- "Top 10 items by value"
- "Average value by category"
- "Distribution by region"

**Comparison**

- "Which has higher revenue: A or B?"
- "Month-over-month growth"
- "Category performance"

### Next Steps

1. **Upload a CSV**: Use the chat interface to upload your data
2. **Explore**: Ask questions about your data structure
3. **Analyze**: Request insights and analysis
4. **Decide**: Make data-driven decisions based on the insights

For more information, see [README.md](../README.md) or [SKILLS.md](../SKILLS.md)
