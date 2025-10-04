#!/usr/bin/env python
"""
Test MongoDB connection using pymongo directly
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()

from decouple import config
import pymongo
from pymongo import MongoClient

def test_mongodb_connection():
    """Test MongoDB connection directly with pymongo"""
    print("Testing MongoDB Connection...")
    print("=" * 50)
    
    try:
        # Get MongoDB URI from environment
        mongodb_uri = config('MONGODB_URI', default='mongodb+srv://username:password@cluster.mongodb.net/disaster_response?retryWrites=true&w=majority')
        mongodb_name = config('MONGODB_NAME', default='disaster_response')
        
        print(f"Connecting to: {mongodb_uri}")
        print(f"Database: {mongodb_name}")
        
        # Create connection
        client = MongoClient(mongodb_uri)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db_list = client.list_database_names()
        print(f"📊 Available databases: {db_list}")
        
        # Test database operations
        db = client[mongodb_name]
        collection = db['test_collection']
        
        # Insert a test document
        test_doc = {
            'name': 'Test Document',
            'message': 'MongoDB connection is working!',
            'timestamp': '2025-01-04T06:30:00Z'
        }
        
        result = collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Find the document
        found_doc = collection.find_one({'_id': result.inserted_id})
        print(f"✅ Document retrieved: {found_doc}")
        
        # Clean up test document
        collection.delete_one({'_id': result.inserted_id})
        print("✅ Test document cleaned up")
        
        # Close connection
        client.close()
        print("✅ Connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == '__main__':
    success = test_mongodb_connection()
    if success:
        print("\n🎉 MongoDB is ready for Django!")
    else:
        print("\n💥 Please check your MongoDB connection settings")
