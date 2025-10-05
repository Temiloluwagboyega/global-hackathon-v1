from mongoengine import Document, fields
from django.utils import timezone
import uuid


class DisasterReport(Document):
	"""
	Model for storing disaster reports with geospatial data.
	"""
	
	DISASTER_TYPE_CHOICES = [
		('flood', 'Flood'),
		('fire', 'Fire'),
		('accident', 'Accident'),
		('collapse', 'Building Collapse'),
	]
	
	STATUS_CHOICES = [
		('active', 'Active'),
		('resolved', 'Resolved'),
		('investigating', 'Under Investigation'),
	]
	
	disaster_type = fields.StringField(
		max_length=20,
		choices=DISASTER_TYPE_CHOICES,
		help_text='Type of disaster incident'
	)
	description = fields.StringField(
		help_text='Detailed description of the incident'
	)
	latitude = fields.FloatField(
		help_text='Latitude coordinate of the incident location'
	)
	longitude = fields.FloatField(
		help_text='Longitude coordinate of the incident location'
	)
	status = fields.StringField(
		max_length=20,
		choices=STATUS_CHOICES,
		default='active',
		help_text='Current status of the incident'
	)
	image = fields.StringField(
		null=True,
		blank=True,
		help_text='Optional image URL of the incident'
	)
	reporter_id = fields.StringField(
		max_length=100,
		null=True,
		blank=True,
		help_text='Optional identifier for the reporter'
	)
	created_at = fields.DateTimeField(
		help_text='When the report was created'
	)
	updated_at = fields.DateTimeField(
		default=timezone.now,
		help_text='When the report was last updated'
	)
	
	meta = {
		'ordering': ['-created_at'],
		'verbose_name': 'Disaster Report',
		'verbose_name_plural': 'Disaster Reports',
		'indexes': [
			'disaster_type',
			'status',
			'created_at',
			('latitude', 'longitude'),
		]
	}
	
	def __str__(self):
		return f'{self.get_disaster_type_display()} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'
	
	def save(self, *args, **kwargs):
		"""Override save to update the updated_at field."""
		self.updated_at = timezone.now()
		return super().save(*args, **kwargs)
	
	@property
	def location(self):
		"""Return location as a dictionary for API responses."""
		return {
			'lat': self.latitude,
			'lng': self.longitude
		}
	
	@property
	def timestamp(self):
		"""Return created_at as ISO string for API responses."""
		timestamp_str = self.created_at.isoformat()
		print(f"Model timestamp property - created_at: {self.created_at}")
		print(f"Model timestamp property - isoformat: {timestamp_str}")
		return timestamp_str
	
	@property
	def image_url(self):
		"""Return the image URL if image exists."""
		return self.image if self.image else None
	
	@property
	def mongodb_id(self):
		"""Return the MongoDB ObjectId as string."""
		return str(self.id)


class WelcomeModalView(Document):
	"""
	Model for tracking which IP addresses have viewed the welcome modal.
	"""
	
	ip_address = fields.StringField(
		max_length=45,  # IPv6 max length
		required=True,
		help_text='IP address of the user'
	)
	user_agent = fields.StringField(
		help_text='User agent string for additional identification'
	)
	viewed_at = fields.DateTimeField(
		default=timezone.now,
		help_text='When the welcome modal was first viewed'
	)
	last_seen = fields.DateTimeField(
		default=timezone.now,
		help_text='When the user was last seen'
	)
	
	meta = {
		'ordering': ['-viewed_at'],
		'verbose_name': 'Welcome Modal View',
		'verbose_name_plural': 'Welcome Modal Views',
		'indexes': [
			'ip_address',
			'viewed_at',
		]
	}
	
	def __str__(self):
		return f'Welcome viewed by {self.ip_address} at {self.viewed_at.strftime("%Y-%m-%d %H:%M")}'
	
	def save(self, *args, **kwargs):
		"""Override save to update the last_seen field."""
		self.last_seen = timezone.now()
		return super().save(*args, **kwargs)