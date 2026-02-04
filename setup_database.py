"""
Database Setup Script
Converts customer orders CSV file to SQLite database
"""

import pandas as pd
import sqlite3
import os

def setup_database():
    """Convert CSV to SQLite database"""
    
    csv_file = 'invoice_data_with_profit.csv'
    db_file = 'orders.db'
    
    # Check if CSV exists
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        print("Please place your CSV file in the project directory and name it 'customer_orders.csv'")
        return
    
    print("📁 Reading CSV file...")
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    print(f"✅ CSV loaded successfully! Found {len(df)} records")
    
    # Display column information
    print("\n📊 Column Information:")
    print("-" * 50)
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        print(f"{i}. {col}")
        print(f"   Type: {dtype}, Non-null: {non_null}/{len(df)}")
    
    # Create SQLite database
    print(f"\n💾 Creating SQLite database: {db_file}")
    conn = sqlite3.connect(db_file)
    
    # Write data to SQLite table
    df.to_sql('orders', conn, if_exists='replace', index=False)
    
    # Verify the data
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    
    print(f"✅ Database created successfully!")
    print(f"   Records in database: {count}")
    
    # Show sample data
    print("\n📋 Sample Data (first 3 rows):")
    print("-" * 50)
    sample_df = pd.read_sql_query("SELECT * FROM orders LIMIT 3", conn)
    print(sample_df.to_string())
    
    conn.close()
    print("\n✅ Setup complete! You can now run: chainlit run app.py -w")

if __name__ == "__main__":
    setup_database()
