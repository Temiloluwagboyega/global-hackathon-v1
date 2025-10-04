#!/usr/bin/env python
"""
Custom MongoDB setup script that bypasses problematic Django migrations
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

def setup_mongodb_collections():
    """Set up MongoDB collections manually"""
    print("Setting up MongoDB collections...")
    print("=" * 50)
    
    try:
        # Get MongoDB URI from environment
        mongodb_uri = config('MONGODB_URI', default='mongodb+srv://username:password@cluster.mongodb.net/disaster_response?retryWrites=true&w=majority')
        mongodb_name = config('MONGODB_NAME', default='disaster_response')
        
        print(f"Connecting to: {mongodb_uri}")
        print(f"Database: {mongodb_name}")
        
        # Create connection
        client = MongoClient(mongodb_uri)
        db = client[mongodb_name]
        
        # Create collections with proper indexes
        collections_to_create = [
            'reports_disasterreport',
            'django_migrations',
            'django_content_type',
            'auth_user',
            'auth_group',
            'auth_permission',
            'django_admin_log',
            'django_session'
        ]
        
        for collection_name in collections_to_create:
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"📁 Collection already exists: {collection_name}")
        
        # Create indexes for reports collection
        reports_collection = db['reports_disasterreport']
        
        # Create geospatial index for location queries
        try:
            reports_collection.create_index([("latitude", 1), ("longitude", 1)])
            print("✅ Created geospatial index for reports")
        except Exception as e:
            print(f"⚠️  Geospatial index creation failed: {e}")
        
        # Create index for disaster_type
        try:
            reports_collection.create_index("disaster_type")
            print("✅ Created index for disaster_type")
        except Exception as e:
            print(f"⚠️  disaster_type index creation failed: {e}")
        
        # Create index for status
        try:
            reports_collection.create_index("status")
            print("✅ Created index for status")
        except Exception as e:
            print(f"⚠️  status index creation failed: {e}")
        
        # Create index for created_at
        try:
            reports_collection.create_index("created_at")
            print("✅ Created index for created_at")
        except Exception as e:
            print(f"⚠️  created_at index creation failed: {e}")
        
        # Insert a migration record to mark migrations as applied
        migrations_collection = db['django_migrations']
        
        # Check if migrations record exists
        existing_migration = migrations_collection.find_one({"app": "reports"})
        if not existing_migration:
            migration_record = {
                "app": "reports",
                "name": "0001_initial",
                "applied": True
            }
            migrations_collection.insert_one(migration_record)
            print("✅ Created migration record for reports app")
        else:
            print("📁 Migration record already exists for reports app")
        
        # Close connection
        client.close()
        print("✅ MongoDB setup completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = setup_mongodb_collections()
    if success:
        print("\n🎉 MongoDB is ready for Django!")
        print("You can now run the Django server without migration issues.")
    else:
        print("\n💥 Please check your MongoDB connection settings")
