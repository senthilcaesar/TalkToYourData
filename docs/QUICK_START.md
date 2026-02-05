# Quick Reference - SQL AI Agent

## Essential Commands

### First Time Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Then edit .env and add your API key

# 5. Setup database
python setup_database.py

# 6. Run the app
chainlit run app.py -w
```

### Daily Use
```bash
# Activate environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the app
chainlit run app.py -w

# Access at: http://localhost:8000
```

## File Checklist

Before running, ensure you have:
- ✅ `customer_orders.csv` - Your data file
- ✅ `.env` - With your ANTHROPIC_API_KEY
- ✅ `venv/` - Virtual environment created
- ✅ All files from the project

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "No module named 'chainlit'" | Activate venv and run `pip install -r requirements.txt` |
| "Database not found" | Run `python setup_database.py` |
| "API key not found" | Check `.env` file exists with correct key |
| App won't start | Ensure port 8000 is free, try `chainlit run app.py --port 8080` |

## Example Questions to Try

### Sales Analysis
- "What are my top 10 products by revenue?"
- "Show me total sales by month"
- "What's the average order value?"

### Geographic
- "Which are my top 5 states by revenue?"
- "How many orders per state?"

### Trends
- "What's the sales trend over time?"
- "Which day of week has highest sales?"

### Products
- "Which products have highest profit margin?"
- "What's my best-selling SKU?"

## Customization Tips

### Change Model
In `app.py`, change:
```python
model="claude-sonnet-4-20250514"
```
to:
```python
model="claude-opus-4-5-20251101"  # More powerful but slower
```

### Increase Result Limit
In `app.py`, find:
```python
display_df = results_df.head(15)
```
Change `15` to desired number.

### Add Visualizations
Install plotly:
```bash
pip install plotly
```

## Useful Keyboard Shortcuts

- `Ctrl+C` - Stop the Chainlit server
- `Ctrl+R` - Refresh browser
- `Ctrl+Shift+I` - Open browser console for debugging

## Project URLs

- Chainlit Docs: https://docs.chainlit.io
- Anthropic API: https://docs.anthropic.com
- Get API Key: https://console.anthropic.com

## Next Steps

1. ✅ Get app running
2. Test with sample questions
3. Customize welcome message
4. Add more example questions
5. Consider adding charts/visualizations
6. Deploy to production (optional)

---

**Pro Tip**: Keep the detailed guide (`sql_agent_guide.md`) open in another window for reference!
