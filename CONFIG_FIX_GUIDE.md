# Quick Fix for Config Error

## The Problem
The config.toml format changed between Chainlit versions. The error you're seeing is about `spontaneous_file_upload` and `edit_message` format.

## Solution: Use the Minimal Config

I've created a simplified config file that works with the latest Chainlit version.

### Step 1: Use the minimal config

```bash
# Copy the minimal config
cp config_minimal.toml .chainlit/config.toml
```

### Step 2: Restart the app

```bash
chainlit run app.py -w
```

## What Changed

**Old format (doesn't work):**
```toml
spontaneous_file_upload = true
edit_message = { enabled = true }
```

**New format (works):**
```toml
[features.spontaneous_file_upload]
enabled = true
accept = ["*/*"]
max_files = 20
max_size_mb = 500
```

## If You Still Get Errors

### Option 1: Delete the .chainlit folder and let it regenerate
```bash
rm -rf .chainlit
chainlit run app.py -w
```

This will create a fresh config, then you can customize it.

### Option 2: Use no custom config at all
```bash
# Just rename or remove the config
mv .chainlit/config.toml .chainlit/config.toml.backup
chainlit run app.py -w
```

The app will work fine with default settings. You'll lose the custom name and colors, but you can add them back gradually.

## Recommended Approach

**Start minimal, add features gradually:**

1. First, get the app running with NO custom config
2. Then add just the UI customization:
   ```toml
   [UI]
   name = "SQL Business Intelligence Agent"
   custom_css = "/public/custom.css"
   ```
3. Then add colors if you want them

## Current Working Config

The `config_minimal.toml` file includes:
- ✅ Custom app name
- ✅ Custom CSS support
- ✅ Theme colors (blue/purple)
- ✅ No problematic features
- ✅ Compatible with latest Chainlit

## Your Files

You have two config options now:
1. **config.toml** - Full featured (updated, should work)
2. **config_minimal.toml** - Minimal, guaranteed to work

Try the minimal one first!

## Quick Commands

```bash
# Use minimal config
cp config_minimal.toml .chainlit/config.toml

# Or start fresh
rm -rf .chainlit

# Run the app
chainlit run app.py -w
```

The custom CSS will still work beautifully even with the minimal config! 🎨
