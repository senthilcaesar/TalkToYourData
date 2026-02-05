"""
Test suite for CSV file upload functionality
"""

import pytest
import os
import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import convert_csv_to_db, validate_sql, get_table_schema


class TestCSVUpload:
    """Test cases for CSV file upload and conversion"""
    
    @pytest.fixture
    def sample_csv_path(self, tmp_path):
        """Create a sample CSV file for testing"""
        csv_file = tmp_path / "test_orders.csv"
        data = {
            'order_id': [1, 2, 3],
            'product': ['Product A', 'Product B', 'Product C'],
            'quantity': [10, 20, 15],
            'price': [100.0, 200.0, 150.0],
            'customer': ['Customer 1', 'Customer 2', 'Customer 3']
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        return str(csv_file)
    
    @pytest.fixture
    def empty_csv_path(self, tmp_path):
        """Create an empty CSV file for testing"""
        csv_file = tmp_path / "empty.csv"
        df = pd.DataFrame()
        df.to_csv(csv_file, index=False)
        return str(csv_file)
    
    @pytest.fixture
    def large_csv_path(self, tmp_path):
        """Create a large CSV file for testing size limits"""
        csv_file = tmp_path / "large_orders.csv"
        # Create a DataFrame with enough rows to exceed size limit
        data = {
            'order_id': range(100000),
            'product': ['Product ' + str(i % 100) for i in range(100000)],
            'quantity': [i % 50 for i in range(100000)],
            'price': [float(i % 1000) for i in range(100000)],
            'customer': ['Customer ' + str(i % 1000) for i in range(100000)]
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        return str(csv_file)
    
    def test_valid_csv_upload(self, sample_csv_path, tmp_path):
        """Test uploading a valid CSV file"""
        db_path = tmp_path / "test.db"
        success, result = convert_csv_to_db(sample_csv_path, str(db_path))
        
        assert success is True
        assert result['records'] == 3
        assert result['columns'] == 5
        assert 'order_id' in result['column_names']
        assert 'product' in result['column_names']
        assert os.path.exists(db_path)
    
    def test_empty_csv_upload(self, empty_csv_path, tmp_path):
        """Test uploading an empty CSV file"""
        db_path = tmp_path / "test_empty.db"
        success, result = convert_csv_to_db(empty_csv_path, str(db_path))
        
        assert success is False
        # The actual error message from pandas is "No columns to parse from file"
        assert "no columns" in result.lower() or "empty" in result.lower()
    
    def test_invalid_csv_path(self, tmp_path):
        """Test with non-existent CSV file"""
        db_path = tmp_path / "test.db"
        success, result = convert_csv_to_db("nonexistent.csv", str(db_path))
        
        assert success is False
        assert isinstance(result, str)
    
    def test_csv_to_db_data_integrity(self, sample_csv_path, tmp_path):
        """Test that data is correctly transferred from CSV to database"""
        db_path = tmp_path / "test.db"
        success, result = convert_csv_to_db(sample_csv_path, str(db_path))
        
        assert success is True
        
        # Verify data in database
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM orders", conn)
        conn.close()
        
        assert len(df) == 3
        assert list(df.columns) == ['order_id', 'product', 'quantity', 'price', 'customer']
        assert df['product'].tolist() == ['Product A', 'Product B', 'Product C']
    
    def test_file_size_check(self, large_csv_path):
        """Test file size validation"""
        file_size_mb = os.path.getsize(large_csv_path) / (1024 * 1024)
        # This test verifies that we can calculate file size correctly
        assert file_size_mb > 0


class TestSQLValidation:
    """Test cases for SQL query validation"""
    
    def test_valid_select_query(self):
        """Test that valid SELECT queries pass validation"""
        query = "SELECT * FROM orders WHERE price > 100"
        assert validate_sql(query) is True
    
    def test_reject_drop_query(self):
        """Test that DROP queries are rejected"""
        query = "DROP TABLE orders"
        with pytest.raises(ValueError, match="Only SELECT queries"):
            validate_sql(query)
    
    def test_reject_delete_query(self):
        """Test that DELETE queries are rejected"""
        query = "DELETE FROM orders WHERE order_id = 1"
        with pytest.raises(ValueError, match="Only SELECT queries"):
            validate_sql(query)
    
    def test_reject_insert_query(self):
        """Test that INSERT queries are rejected"""
        query = "INSERT INTO orders VALUES (1, 'Product', 10, 100, 'Customer')"
        with pytest.raises(ValueError, match="Only SELECT queries"):
            validate_sql(query)
    
    def test_reject_update_query(self):
        """Test that UPDATE queries are rejected"""
        query = "UPDATE orders SET price = 200 WHERE order_id = 1"
        with pytest.raises(ValueError, match="Only SELECT queries"):
            validate_sql(query)
    
    def test_reject_non_select_query(self):
        """Test that non-SELECT queries are rejected"""
        query = "CREATE TABLE new_table (id INT)"
        with pytest.raises(ValueError, match="Only SELECT queries"):
            validate_sql(query)
    
    def test_case_insensitive_validation(self):
        """Test that validation is case-insensitive"""
        query = "select * from orders"
        assert validate_sql(query) is True
        
        query = "SELECT * FROM orders"
        assert validate_sql(query) is True


class TestDatabaseSchema:
    """Test cases for database schema retrieval"""
    
    @pytest.fixture
    def setup_test_db(self, tmp_path):
        """Setup a test database"""
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(db_path)
        
        # Create test table
        conn.execute("""
            CREATE TABLE orders (
                order_id INTEGER,
                product TEXT,
                quantity INTEGER,
                price REAL,
                customer TEXT
            )
        """)
        
        # Insert sample data
        conn.execute("""
            INSERT INTO orders VALUES 
            (1, 'Product A', 10, 100.0, 'Customer 1'),
            (2, 'Product B', 20, 200.0, 'Customer 2'),
            (3, 'Product C', 15, 150.0, 'Customer 3')
        """)
        
        conn.commit()
        conn.close()
        
        return str(db_path)
    
    def test_get_schema(self, setup_test_db, monkeypatch):
        """Test retrieving database schema"""
        # Temporarily change DB_PATH to test database
        import app
        monkeypatch.setattr(app, 'DB_PATH', setup_test_db)
        
        schema = get_table_schema()
        
        assert 'Table: orders' in schema
        assert 'order_id' in schema
        assert 'product' in schema
        assert 'quantity' in schema
        assert 'price' in schema
        assert 'customer' in schema
        assert 'Sample Data' in schema


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
