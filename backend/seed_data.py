#!/usr/bin/env python
"""
Seed script to populate the database with sample disaster reports.
Run this script after setting up the database and running migrations.
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()

from reports.models import DisasterReport


def create_sample_reports():
	"""
	Create sample disaster reports for testing.
	"""
	
	# Sample data for different disaster types
	sample_data = [
		{
			'disaster_type': 'flood',
			'descriptions': [
				'Heavy rainfall causing severe flooding in residential area. Water level rising rapidly.',
				'River overflow affecting multiple neighborhoods. Emergency evacuation in progress.',
				'Flash flood reported in downtown area. Several vehicles stranded.',
				'Damaged drainage system causing water accumulation on main street.',
			],
			'locations': [
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos, Nigeria
				{'lat': 6.4474, 'lng': 3.3903},  # Lagos Island
				{'lat': 6.4654, 'lng': 3.4064},  # Victoria Island
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos Mainland
			]
		},
		{
			'disaster_type': 'fire',
			'descriptions': [
				'Building fire reported in commercial district. Smoke visible from several blocks away.',
				'Vehicle fire on highway causing traffic disruption.',
				'Electrical fire in residential building. Residents evacuated safely.',
				'Wildfire spreading near forest area. Fire department responding.',
			],
			'locations': [
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos, Nigeria
				{'lat': 6.4474, 'lng': 3.3903},  # Lagos Island
				{'lat': 6.4654, 'lng': 3.4064},  # Victoria Island
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos Mainland
			]
		},
		{
			'disaster_type': 'accident',
			'descriptions': [
				'Multi-vehicle collision on major highway. Emergency services on scene.',
				'Pedestrian accident reported near school zone.',
				'Motorcycle accident at busy intersection. Traffic backed up.',
				'Construction vehicle accident on work site.',
			],
			'locations': [
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos, Nigeria
				{'lat': 6.4474, 'lng': 3.3903},  # Lagos Island
				{'lat': 6.4654, 'lng': 3.4064},  # Victoria Island
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos Mainland
			]
		},
		{
			'disaster_type': 'collapse',
			'descriptions': [
				'Building collapse reported in residential area. Search and rescue in progress.',
				'Bridge collapse affecting traffic flow. Alternative routes recommended.',
				'Wall collapse at construction site. No injuries reported.',
				'Roof collapse due to structural damage. Building evacuated.',
			],
			'locations': [
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos, Nigeria
				{'lat': 6.4474, 'lng': 3.3903},  # Lagos Island
				{'lat': 6.4654, 'lng': 3.4064},  # Victoria Island
				{'lat': 6.5244, 'lng': 3.3792},  # Lagos Mainland
			]
		}
	]
	
	# Status choices
	status_choices = ['active', 'resolved', 'investigating']
	
	# Create reports
	reports_created = 0
	
	for disaster_type_data in sample_data:
		disaster_type = disaster_type_data['disaster_type']
		descriptions = disaster_type_data['descriptions']
		locations = disaster_type_data['locations']
		
		# Create 3-5 reports for each disaster type
		num_reports = random.randint(3, 5)
		
		for i in range(num_reports):
			# Random description and location
			description = random.choice(descriptions)
			location = random.choice(locations)
			
			# Add some random variation to coordinates
			lat = location['lat'] + random.uniform(-0.01, 0.01)
			lng = location['lng'] + random.uniform(-0.01, 0.01)
			
			# Random status
			status = random.choice(status_choices)
			
			# Random creation time (within last 7 days)
			created_at = datetime.now() - timedelta(
				days=random.randint(0, 7),
				hours=random.randint(0, 23),
				minutes=random.randint(0, 59)
			)
			
			# Create the report
			report = DisasterReport.objects.create(
				disaster_type=disaster_type,
				description=description,
				latitude=lat,
				longitude=lng,
				status=status,
				reporter_id=f'reporter_{random.randint(1000, 9999)}',
				created_at=created_at
			)
			
			reports_created += 1
			print(f'Created {disaster_type} report: {report.id}')
	
	print(f'\nSuccessfully created {reports_created} sample reports!')
	return reports_created


def clear_existing_reports():
	"""
	Clear all existing reports (optional).
	"""
	confirm = input('Do you want to clear existing reports? (y/N): ')
	if confirm.lower() == 'y':
		count = DisasterReport.objects.count()
		DisasterReport.objects.all().delete()
		print(f'Cleared {count} existing reports.')
		return True
	return False


def main():
	"""
	Main function to run the seed script.
	"""
	print('Disaster Response API - Seed Data Script')
	print('=' * 50)
	
	# Check if reports already exist
	existing_count = DisasterReport.objects.count()
	if existing_count > 0:
		print(f'Found {existing_count} existing reports.')
		if not clear_existing_reports():
			print('Keeping existing reports and adding new ones.')
	
	# Create sample reports
	try:
		reports_created = create_sample_reports()
		print(f'\nSeed script completed successfully!')
		print(f'Total reports in database: {DisasterReport.objects.count()}')
		
	except Exception as e:
		print(f'Error creating sample reports: {e}')
		sys.exit(1)


if __name__ == '__main__':
	main()
