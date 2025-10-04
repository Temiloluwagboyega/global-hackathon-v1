#!/usr/bin/env python
"""
Deployment script for Disaster Response API.
This script helps with common deployment tasks.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()


def run_command(command, description):
	"""Run a shell command and handle errors."""
	print(f"🔄 {description}...")
	try:
		result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
		print(f"✅ {description} completed successfully")
		return True
	except subprocess.CalledProcessError as e:
		print(f"❌ {description} failed: {e}")
		print(f"Error output: {e.stderr}")
		return False


def check_environment():
	"""Check if environment is properly configured."""
	print("🔍 Checking environment configuration...")
	
	# Check if .env file exists
	env_file = Path('.env')
	if not env_file.exists():
		print("⚠️  .env file not found. Please copy env.example to .env and configure it.")
		return False
	
	# Check required environment variables
	required_vars = ['SECRET_KEY', 'MONGODB_URI', 'MONGODB_NAME']
	missing_vars = []
	
	for var in required_vars:
		if not os.getenv(var):
			missing_vars.append(var)
	
	if missing_vars:
		print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
		return False
	
	print("✅ Environment configuration looks good")
	return True


def install_dependencies():
	"""Install Python dependencies."""
	return run_command("pip install -r requirements.txt", "Installing dependencies")


def run_migrations():
	"""Run Django migrations."""
	success = run_command("python manage.py makemigrations", "Creating migrations")
	if not success:
		return False
	
	return run_command("python manage.py migrate", "Running migrations")


def collect_static():
	"""Collect static files for production."""
	return run_command("python manage.py collectstatic --noinput", "Collecting static files")


def create_superuser():
	"""Create a superuser account."""
	print("👤 Creating superuser account...")
	try:
		# Check if superuser already exists
		from django.contrib.auth import get_user_model
		User = get_user_model()
		if User.objects.filter(is_superuser=True).exists():
			print("✅ Superuser already exists")
			return True
		
		# Create superuser
		from django.core.management import call_command
		call_command('createsuperuser', interactive=False, username='admin', email='admin@example.com')
		print("✅ Superuser created successfully")
		return True
	except Exception as e:
		print(f"❌ Failed to create superuser: {e}")
		return False


def seed_database():
	"""Seed the database with sample data."""
	print("🌱 Seeding database with sample data...")
	try:
		from seed_data import create_sample_reports
		reports_created = create_sample_reports()
		print(f"✅ Created {reports_created} sample reports")
		return True
	except Exception as e:
		print(f"❌ Failed to seed database: {e}")
		return False


def run_tests():
	"""Run the test suite."""
	return run_command("python manage.py test", "Running tests")


def start_server():
	"""Start the development server."""
	print("🚀 Starting development server...")
	print("📱 API will be available at: http://localhost:8000/api/")
	print("📚 API Documentation: http://localhost:8000/api/docs/")
	print("🔧 Admin Panel: http://localhost:8000/admin/")
	print("\nPress Ctrl+C to stop the server")
	
	try:
		subprocess.run("python manage.py runserver", shell=True)
	except KeyboardInterrupt:
		print("\n👋 Server stopped")


def main():
	"""Main deployment function."""
	print("🚀 Disaster Response API - Deployment Script")
	print("=" * 50)
	
	# Check environment
	if not check_environment():
		print("\n❌ Environment check failed. Please fix the issues above.")
		return
	
	# Install dependencies
	if not install_dependencies():
		print("\n❌ Dependency installation failed.")
		return
	
	# Run migrations
	if not run_migrations():
		print("\n❌ Migration failed.")
		return
	
	# Collect static files (for production)
	if os.getenv('DEBUG', 'True').lower() == 'false':
		if not collect_static():
			print("\n❌ Static file collection failed.")
			return
	
	# Create superuser
	create_superuser()
	
	# Seed database
	seed_database()
	
	# Run tests
	run_tests()
	
	print("\n🎉 Deployment completed successfully!")
	print("\nNext steps:")
	print("1. Update your .env file with MongoDB Atlas connection string")
	print("2. Run 'python manage.py runserver' to start the development server")
	print("3. Visit http://localhost:8000/api/docs/ to see the API documentation")
	
	# Ask if user wants to start server
	start_server_choice = input("\nDo you want to start the development server now? (y/N): ")
	if start_server_choice.lower() == 'y':
		start_server()


if __name__ == '__main__':
	main()
