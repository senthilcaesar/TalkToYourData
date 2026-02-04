# UI Customization Setup Instructions

## Step 1: Setup Chainlit Configuration

1. **Create the `.chainlit` folder** in your project root:
   ```bash
   mkdir -p .chainlit
   ```

2. **Copy the config file**:
   ```bash
   cp config.toml .chainlit/config.toml
   ```

3. **Create public folder for assets**:
   ```bash
   mkdir -p public
   ```

4. **Copy the custom CSS**:
   ```bash
   cp custom.css public/custom.css
   ```

## Step 2: Add Your Logo (Optional)

Place your logo files in the `public` folder:
- `logo_light.png` - For light mode (200x50px recommended)
- `logo_dark.png` - For dark mode (200x50px recommended)
- `favicon.png` - Browser tab icon (32x32px)

If you don't have logos, you can:
1. Create them with tools like Canva
2. Use text-based logos
3. Skip this step for now

## Step 3: Restart Your App

```bash
chainlit run app.py -w
```

## Your Project Structure Should Look Like:

```
sql-ai-agent/
├── .chainlit/
│   └── config.toml          ← Chainlit configuration
├── public/
│   ├── custom.css           ← Your custom styles
│   ├── logo_light.png       ← (optional) Light mode logo
│   ├── logo_dark.png        ← (optional) Dark mode logo
│   └── favicon.png          ← (optional) Browser icon
├── venv/
├── app.py
├── setup_database.py
├── requirements.txt
├── .env
├── customer_orders.csv
└── orders.db
```

## Customization Tips

### Change Colors

Edit `.chainlit/config.toml`, section `[UI.theme.light.primary]`:

```toml
[UI.theme.light.primary]
    main = "#2563EB"      # Primary color
    dark = "#1E40AF"      # Darker shade
    light = "#3B82F6"     # Lighter shade
```

**Color Examples:**
- Blue: `#2563EB` (current)
- Purple: `#7C3AED`
- Green: `#059669`
- Red: `#DC2626`
- Orange: `#EA580C`

### Change Font

Edit `public/custom.css`, change the import:

```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
```

Then update the font-family:
```css
#root {
    font-family: 'Poppins', sans-serif;
}
```

**Popular Font Choices:**
- Inter (current - modern, clean)
- Poppins (friendly, rounded)
- Roboto (classic, readable)
- Montserrat (bold, geometric)

### Customize Welcome Message

Edit `app.py`, find the `@cl.on_chat_start` function and customize the welcome message.

### Add Gradient Backgrounds

In `public/custom.css`, you can change the gradient colors:

```css
background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
```

**Gradient Examples:**
- Blue-Purple: `#667eea 0%, #764ba2 100%` (current)
- Ocean: `#2E3192 0%, #1BFFFF 100%`
- Sunset: `#FF512F 0%, #DD2476 100%`
- Forest: `#134E5E 0%, #71B280 100%`

## Testing Your Changes

1. Save your changes
2. Restart the app: `chainlit run app.py -w`
3. Hard refresh your browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

## Troubleshooting

**CSS not loading?**
- Make sure `public/custom.css` exists
- Check the path in `.chainlit/config.toml`
- Hard refresh browser

**Config not applying?**
- Verify `.chainlit/config.toml` exists
- Check for TOML syntax errors
- Restart the app completely

**Logos not showing?**
- Check file names match exactly
- Verify files are in `public/` folder
- Check file permissions

## Next Level: Add Charts

Want to add interactive charts? Install plotly:

```bash
pip install plotly kaleido
```

Then you can generate charts in your responses!

## Need Help?

- Check Chainlit docs: https://docs.chainlit.io/customization/overview
- Explore CSS examples in `custom.css`
- Experiment with colors and fonts

Enjoy your beautiful AI agent! 🎨✨
