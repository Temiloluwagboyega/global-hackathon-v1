from django.core.management.base import BaseCommand
from reports.models import DisasterReport
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
	help = 'Seed the database with sample disaster reports'
	
	def add_arguments(self, parser):
		parser.add_argument(
			'--clear',
			action='store_true',
			help='Clear existing reports before seeding',
		)
		parser.add_argument(
			'--count',
			type=int,
			default=20,
			help='Number of reports to create (default: 20)',
		)
	
	def handle(self, *args, **options):
		clear_existing = options['clear']
		count = options['count']
		
		if clear_existing:
			existing_count = DisasterReport.objects.count()
			DisasterReport.objects.all().delete()
			self.stdout.write(
				self.style.SUCCESS(f'Cleared {existing_count} existing reports')
			)
		
		# Sample data
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
				]
			}
		]
		
		status_choices = ['active', 'resolved', 'investigating']
		reports_created = 0
		
		for i in range(count):
			# Random disaster type
			disaster_data = random.choice(sample_data)
			disaster_type = disaster_data['disaster_type']
			description = random.choice(disaster_data['descriptions'])
			location = random.choice(disaster_data['locations'])
			
			# Add random variation to coordinates
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
		
		self.stdout.write(
			self.style.SUCCESS(f'Successfully created {reports_created} sample reports!')
		)
		self.stdout.write(
			self.style.SUCCESS(f'Total reports in database: {DisasterReport.objects.count()}')
		)
