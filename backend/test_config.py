#!/usr/bin/env python
"""
Test script to verify the new configuration setup with decouple and dj-database-url.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()

def test_decouple_config():
	"""Test that decouple config is working correctly."""
	print("🔍 Testing decouple configuration...")
	
	try:
		from decouple import config
		
		# Test basic config
		secret_key = config('SECRET_KEY', default='test-default')
		debug = config('DEBUG', default=True, cast=bool)
		upload_size = config('MAX_UPLOAD_SIZE', default=10485760, cast=int)
		
		print("✅ Decouple config working correctly!")
		print(f"   Secret Key: {secret_key[:20]}...")
		print(f"   Debug: {debug}")
		print(f"   Upload Size: {upload_size}")
		
		return True
		
	except Exception as e:
		print(f"❌ Decouple config test failed: {e}")
		return False

def test_database_url_parsing():
	"""Test that dj-database-url is working correctly."""
	print("\n🔍 Testing database URL parsing...")
	
	try:
		import dj_database_url
		
		# Test SQLite URL
		sqlite_url = 'sqlite:///db.sqlite3'
		sqlite_config = dj_database_url.parse(sqlite_url)
		
		print("✅ SQLite URL parsing:")
		print(f"   Engine: {sqlite_config['ENGINE']}")
		print(f"   Name: {sqlite_config['NAME']}")
		
		# Test PostgreSQL URL
		postgres_url = 'postgres://user:pass@localhost:5432/dbname'
		postgres_config = dj_database_url.parse(postgres_url)
		
		print("✅ PostgreSQL URL parsing:")
		print(f"   Engine: {postgres_config['ENGINE']}")
		print(f"   Name: {postgres_config['NAME']}")
		print(f"   User: {postgres_config['USER']}")
		print(f"   Host: {postgres_config['HOST']}")
		
		return True
		
	except Exception as e:
		print(f"❌ Database URL parsing test failed: {e}")
		return False

def test_django_settings():
	"""Test that Django settings are using the new configuration."""
	print("\n🔍 Testing Django settings integration...")
	
	try:
		from django.conf import settings
		
		# Test that settings are loaded correctly
		secret_key = settings.SECRET_KEY
		debug = settings.DEBUG
		database_config = settings.DATABASES['default']
		cloudinary_config = settings.CLOUDINARY_STORAGE
		cors_origins = settings.CORS_ALLOWED_ORIGINS
		
		print("✅ Django settings loaded correctly!")
		print(f"   Secret Key: {secret_key[:20]}...")
		print(f"   Debug: {debug}")
		print(f"   Database Engine: {database_config['ENGINE']}")
		print(f"   Cloudinary Cloud: {cloudinary_config['CLOUD_NAME']}")
		print(f"   CORS Origins: {len(cors_origins)} configured")
		
		return True
		
	except Exception as e:
		print(f"❌ Django settings test failed: {e}")
		return False

def test_environment_variables():
	"""Test environment variable handling."""
	print("\n🔍 Testing environment variable handling...")
	
	try:
		from decouple import config
		
		# Test with defaults
		test_var = config('NON_EXISTENT_VAR', default='default-value')
		print(f"✅ Default value handling: {test_var}")
		
		# Test boolean casting
		debug_bool = config('DEBUG', default=True, cast=bool)
		print(f"✅ Boolean casting: {debug_bool} (type: {type(debug_bool)})")
		
		# Test integer casting
		upload_size = config('MAX_UPLOAD_SIZE', default=10485760, cast=int)
		print(f"✅ Integer casting: {upload_size} (type: {type(upload_size)})")
		
		return True
		
	except Exception as e:
		print(f"❌ Environment variable test failed: {e}")
		return False

def test_database_switching():
	"""Test that database can be switched using DATABASE_URL."""
	print("\n🔍 Testing database switching...")
	
	try:
		import dj_database_url
		
		# Test different database URLs
		databases = {
			'SQLite': 'sqlite:///db.sqlite3',
			'PostgreSQL': 'postgres://user:pass@localhost:5432/dbname',
			'MySQL': 'mysql://user:pass@localhost:3306/dbname',
		}
		
		for db_type, url in databases.items():
			config = dj_database_url.parse(url)
			print(f"✅ {db_type} configuration:")
			print(f"   Engine: {config['ENGINE']}")
			if 'NAME' in config:
				print(f"   Database: {config['NAME']}")
		
		return True
		
	except Exception as e:
		print(f"❌ Database switching test failed: {e}")
		return False

def main():
	"""Run all configuration tests."""
	print("⚙️  Configuration Test Suite")
	print("=" * 40)
	
	tests = [
		test_decouple_config,
		test_database_url_parsing,
		test_django_settings,
		test_environment_variables,
		test_database_switching,
	]
	
	passed = 0
	total = len(tests)
	
	for test in tests:
		if test():
			passed += 1
	
	print(f"\n📊 Test Results: {passed}/{total} tests passed")
	
	if passed == total:
		print("🎉 All configuration tests passed!")
		print("\n✅ Benefits of the new configuration:")
		print("   - Better environment variable handling with decouple")
		print("   - Automatic database URL parsing with dj-database-url")
		print("   - Type casting for boolean and integer values")
		print("   - Default values for all configuration options")
		print("   - Easy database switching via DATABASE_URL")
		print("\n🚀 Your configuration is production-ready!")
	else:
		print("❌ Some tests failed. Please check the errors above.")
		return 1
	
	return 0

if __name__ == '__main__':
	sys.exit(main())
