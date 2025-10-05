from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reports.models import DisasterReport


class Command(BaseCommand):
	help = 'Delete resolved reports that have been resolved for more than 10 minutes'

	def add_arguments(self, parser):
		parser.add_argument(
			'--dry-run',
			action='store_true',
			help='Show what would be deleted without actually deleting',
		)

	def handle(self, *args, **options):
		# Calculate the cutoff time (10 minutes ago)
		cutoff_time = timezone.now() - timedelta(minutes=10)
		
		# Find resolved reports that were updated more than 10 minutes ago
		resolved_reports = DisasterReport.objects.filter(
			status='resolved',
			updated_at__lt=cutoff_time
		)
		
		count = resolved_reports.count()
		
		if count == 0:
			self.stdout.write(
				self.style.SUCCESS('No resolved reports found to delete.')
			)
			return
		
		if options['dry_run']:
			self.stdout.write(
				self.style.WARNING(f'DRY RUN: Would delete {count} resolved reports:')
			)
			for report in resolved_reports:
				self.stdout.write(
					f'  - {report.get_disaster_type_display()} (ID: {report.id}) - '
					f'Resolved: {report.updated_at.strftime("%Y-%m-%d %H:%M:%S")}'
				)
		else:
			# Log the reports being deleted
			self.stdout.write(f'Deleting {count} resolved reports:')
			for report in resolved_reports:
				self.stdout.write(
					f'  - {report.get_disaster_type_display()} (ID: {report.id}) - '
					f'Resolved: {report.updated_at.strftime("%Y-%m-%d %H:%M:%S")}'
				)
			
			# Delete the reports
			deleted_count, _ = resolved_reports.delete()
			
			self.stdout.write(
				self.style.SUCCESS(
					f'Successfully deleted {deleted_count} resolved reports.'
				)
			)
