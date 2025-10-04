#!/usr/bin/env python
"""
Test script to verify the Django setup is working correctly.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()

def test_imports():
	"""Test that all modules can be imported."""
	print("🔍 Testing imports...")
	
	try:
		from reports.models import DisasterReport
		print("✅ Models imported successfully")
	except ImportError as e:
		print(f"❌ Failed to import models: {e}")
		return False
	
	try:
		from reports.serializers import DisasterReportSerializer
		print("✅ Serializers imported successfully")
	except ImportError as e:
		print(f"❌ Failed to import serializers: {e}")
		return False
	
	try:
		from reports.views import ReportsListView
		print("✅ Views imported successfully")
	except ImportError as e:
		print(f"❌ Failed to import views: {e}")
		return False
	
	return True

def test_model_creation():
	"""Test that the model can be created."""
	print("\n🔍 Testing model creation...")
	
	try:
		from reports.models import DisasterReport
		
		# Test model creation (without saving to DB)
		report = DisasterReport(
			disaster_type='flood',
			description='Test flood report',
			latitude=6.5244,
			longitude=3.3792,
			status='active'
		)
		
		# Test properties
		location = report.location
		timestamp = report.timestamp
		
		print("✅ Model creation and properties work correctly")
		print(f"   Location: {location}")
		print(f"   Timestamp: {timestamp}")
		return True
		
	except Exception as e:
		print(f"❌ Model creation failed: {e}")
		return False

def test_serializer():
	"""Test that serializers work correctly."""
	print("\n🔍 Testing serializers...")
	
	try:
		from reports.models import DisasterReport
		from reports.serializers import DisasterReportSerializer
		
		# Create a test report
		report = DisasterReport(
			disaster_type='fire',
			description='Test fire report',
			latitude=6.5244,
			longitude=3.3792,
			status='active'
		)
		
		# Test serialization
		serializer = DisasterReportSerializer(report)
		data = serializer.data
		
		print("✅ Serializer works correctly")
		print(f"   Serialized data keys: {list(data.keys())}")
		return True
		
	except Exception as e:
		print(f"❌ Serializer test failed: {e}")
		return False

def test_settings():
	"""Test that Django settings are configured correctly."""
	print("\n🔍 Testing Django settings...")
	
	try:
		from django.conf import settings
		
		# Check key settings
		installed_apps = settings.INSTALLED_APPS
		middleware = settings.MIDDLEWARE
		
		required_apps = ['rest_framework', 'corsheaders', 'drf_spectacular', 'reports']
		required_middleware = ['corsheaders.middleware.CorsMiddleware']
		
		missing_apps = [app for app in required_apps if app not in installed_apps]
		missing_middleware = [mw for mw in required_middleware if mw not in middleware]
		
		if missing_apps:
			print(f"❌ Missing apps: {missing_apps}")
			return False
		
		if missing_middleware:
			print(f"❌ Missing middleware: {missing_middleware}")
			return False
		
		print("✅ Django settings configured correctly")
		print(f"   Installed apps: {len(installed_apps)}")
		print(f"   Middleware: {len(middleware)}")
		return True
		
	except Exception as e:
		print(f"❌ Settings test failed: {e}")
		return False

def main():
	"""Run all tests."""
	print("🚀 Disaster Response API - Setup Test")
	print("=" * 50)
	
	tests = [
		test_imports,
		test_settings,
		test_model_creation,
		test_serializer,
	]
	
	passed = 0
	total = len(tests)
	
	for test in tests:
		if test():
			passed += 1
	
	print(f"\n📊 Test Results: {passed}/{total} tests passed")
	
	if passed == total:
		print("🎉 All tests passed! The setup is working correctly.")
		print("\nNext steps:")
		print("1. Run 'python manage.py makemigrations' to create migrations")
		print("2. Run 'python manage.py migrate' to apply migrations")
		print("3. Run 'python manage.py runserver' to start the development server")
		print("4. Visit http://localhost:8000/api/docs/ to see the API documentation")
	else:
		print("❌ Some tests failed. Please check the errors above.")
		return 1
	
	return 0

if __name__ == '__main__':
	sys.exit(main())
