#!/usr/bin/env python3
"""
Simple script to cleanup resolved reports.
Can be run via cron job or scheduled task.
"""

import os
import sys
import django
from datetime import timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_response.settings')
django.setup()

from django.core.management import call_command
from django.utils import timezone
from reports.models import DisasterReport


def cleanup_resolved_reports():
	"""
	Cleanup resolved reports that have been resolved for more than 10 minutes.
	"""
	try:
		# Calculate the cutoff time (10 minutes ago)
		cutoff_time = timezone.now() - timedelta(minutes=10)
		
		# Find resolved reports that were updated more than 10 minutes ago
		resolved_reports = DisasterReport.objects.filter(
			status='resolved',
			updated_at__lt=cutoff_time
		)
		
		count = resolved_reports.count()
		
		if count == 0:
			print(f"[{timezone.now()}] No resolved reports found to delete.")
			return
		
		print(f"[{timezone.now()}] Found {count} resolved reports to delete:")
		
		# Log the reports being deleted
		for report in resolved_reports:
			print(f"  - {report.get_disaster_type_display()} (ID: {report.id}) - "
				  f"Resolved: {report.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
		
		# Delete the reports
		deleted_count = resolved_reports.delete()
		
		print(f"[{timezone.now()}] Successfully deleted {deleted_count} resolved reports.")
		
	except Exception as e:
		print(f"[{timezone.now()}] Error during cleanup: {str(e)}")
		sys.exit(1)


if __name__ == '__main__':
	cleanup_resolved_reports()
