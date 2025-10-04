#!/usr/bin/env python
"""
Simple database connection test for debugging
"""
import os
import sys
import django
from decouple import config

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()

from django.db import connection
from reports.models import DisasterReport

def test_connection():
    """Test database connection and basic operations"""
    try:
        print("Testing database connection...")
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✓ Connection test passed: {result}")
        
        # Test model operations
        print("Testing model operations...")
        
        # Count existing reports
        count = DisasterReport.objects.count()
        print(f"✓ Model count test passed: {count} reports found")
        
        # Test creating a simple report (without saving)
        test_report = DisasterReport(
            disaster_type='test',
            description='Test report',
            latitude=0.0,
            longitude=0.0,
            status='active'
        )
        print("✓ Model creation test passed")
        
        print("All tests passed! Database is working correctly.")
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_connection()
