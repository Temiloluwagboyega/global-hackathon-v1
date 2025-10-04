#!/usr/bin/env python
"""
Test MongoDB SSL connection
"""
import os
import sys
import ssl
from decouple import config

# Fix SSL context
ssl._create_default_https_context = ssl._create_unverified_context

try:
    import pymongo
    from pymongo import MongoClient
    
    print("Testing MongoDB SSL connection...")
    
    # Get MongoDB URI
    mongodb_uri = config('MONGODB_URI')
    print(f"Connecting to: {mongodb_uri[:50]}...")
    
    # Create client with SSL settings
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=20000,
        socketTimeoutMS=30000,
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
    )
    
    # Test connection
    client.admin.command('ping')
    print("✓ MongoDB connection successful!")
    
    # Test database access
    db = client[config('MONGODB_NAME')]
    collections = db.list_collection_names()
    print(f"✓ Database access successful! Collections: {collections}")
    
    client.close()
    
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    import traceback
    traceback.print_exc()
