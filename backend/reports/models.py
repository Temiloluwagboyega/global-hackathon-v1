from django.db import models
from django.utils import timezone
import uuid


class DisasterReport(models.Model):
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
	
	id = models.AutoField(primary_key=True)
	disaster_type = models.CharField(
		max_length=20,
		choices=DISASTER_TYPE_CHOICES,
		help_text='Type of disaster incident'
	)
	description = models.TextField(
		help_text='Detailed description of the incident'
	)
	latitude = models.FloatField(
		help_text='Latitude coordinate of the incident location'
	)
	longitude = models.FloatField(
		help_text='Longitude coordinate of the incident location'
	)
	status = models.CharField(
		max_length=20,
		choices=STATUS_CHOICES,
		default='active',
		help_text='Current status of the incident'
	)
	image = models.ImageField(
		upload_to='disaster_images/',
		null=True,
		blank=True,
		help_text='Optional image of the incident',
		storage=None,  # Will use Cloudinary in production
	)
	reporter_id = models.CharField(
		max_length=100,
		null=True,
		blank=True,
		help_text='Optional identifier for the reporter'
	)
	created_at = models.DateTimeField(
		default=timezone.now,
		help_text='When the report was created'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		help_text='When the report was last updated'
	)
	
	class Meta:
		ordering = ['-created_at']
		verbose_name = 'Disaster Report'
		verbose_name_plural = 'Disaster Reports'
		indexes = [
			models.Index(fields=['disaster_type']),
			models.Index(fields=['status']),
			models.Index(fields=['created_at']),
			models.Index(fields=['latitude', 'longitude']),
		]
	
	def __str__(self):
		return f'{self.get_disaster_type_display()} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'
	
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
		return self.created_at.isoformat()
	
	@property
	def image_url(self):
		"""Return the image URL if image exists."""
		if self.image:
			return self.image.url
		return None
	
	@property
	def mongodb_id(self):
		"""Return a unique ID based on report content and timestamp."""
		import hashlib
		# Create a unique ID based on report content and timestamp
		content = f"{self.disaster_type}_{self.description}_{self.latitude}_{self.longitude}_{self.created_at.isoformat()}"
		return hashlib.md5(content.encode()).hexdigest()[:24]  # 24 chars like MongoDB ObjectId