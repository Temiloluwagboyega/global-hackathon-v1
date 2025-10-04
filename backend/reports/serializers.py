from rest_framework import serializers
from .models import DisasterReport


class DisasterReportSerializer(serializers.ModelSerializer):
	"""
	Serializer for DisasterReport model.
	"""
	id = serializers.CharField(read_only=True)  # Handle MongoDB ObjectId as string
	location = serializers.SerializerMethodField()
	timestamp = serializers.SerializerMethodField()
	image_url = serializers.SerializerMethodField()
	
	class Meta:
		model = DisasterReport
		fields = [
			'id',
			'disaster_type',
			'description',
			'location',
			'timestamp',
			'image_url',
			'status',
			'reporter_id',
		]
		read_only_fields = ['id', 'created_at', 'updated_at']
	
	def get_location(self, obj):
		"""Return location as a dictionary."""
		return obj.location
	
	def get_timestamp(self, obj):
		"""Return timestamp as ISO string."""
		return obj.timestamp
	
	def get_image_url(self, obj):
		"""Return image URL if exists."""
		return obj.image_url
	
	def to_representation(self, instance):
		"""Customize the representation to match frontend expectations."""
		data = super().to_representation(instance)
		# Map disaster_type to type for frontend compatibility
		data['type'] = instance.disaster_type
		
		# Handle MongoDB ObjectId conversion
		if hasattr(instance, 'id') and instance.id:
			# Convert ObjectId to string for JSON serialization
			data['id'] = str(instance.id)
		
		return data


class CreateDisasterReportSerializer(serializers.ModelSerializer):
	"""
	Serializer for creating new disaster reports.
	"""
	latitude = serializers.FloatField(write_only=True)
	longitude = serializers.FloatField(write_only=True)
	type = serializers.CharField(source='disaster_type', write_only=True)
	
	class Meta:
		model = DisasterReport
		fields = [
			'type',
			'description',
			'latitude',
			'longitude',
			'image',
			'reporter_id',
		]
	
	def validate_latitude(self, value):
		"""Validate latitude is within valid range."""
		if not -90 <= value <= 90:
			raise serializers.ValidationError('Latitude must be between -90 and 90 degrees.')
		return value
	
	def validate_longitude(self, value):
		"""Validate longitude is within valid range."""
		if not -180 <= value <= 180:
			raise serializers.ValidationError('Longitude must be between -180 and 180 degrees.')
		return value
	
	def validate_type(self, value):
		"""Validate disaster type is valid."""
		valid_types = [choice[0] for choice in DisasterReport.DISASTER_TYPE_CHOICES]
		if value not in valid_types:
			raise serializers.ValidationError(f'Invalid disaster type. Must be one of: {", ".join(valid_types)}')
		return value


class UpdateReportStatusSerializer(serializers.ModelSerializer):
	"""
	Serializer for updating report status.
	"""
	
	class Meta:
		model = DisasterReport
		fields = ['status']
	
	def validate_status(self, value):
		"""Validate status is valid."""
		valid_statuses = [choice[0] for choice in DisasterReport.STATUS_CHOICES]
		if value not in valid_statuses:
			raise serializers.ValidationError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
		return value


class AISummarySerializer(serializers.Serializer):
	"""
	Serializer for AI summary response.
	"""
	summary = serializers.CharField()
	last24Hours = serializers.DictField()
	location = serializers.CharField()
	generatedAt = serializers.DateTimeField()
	
	def to_representation(self, instance):
		"""Customize the representation."""
		data = super().to_representation(instance)
		# Convert datetime to ISO string
		if 'generatedAt' in data:
			data['generatedAt'] = data['generatedAt'].isoformat()
		return data


class ReportsResponseSerializer(serializers.Serializer):
	"""
	Serializer for reports list response.
	"""
	reports = DisasterReportSerializer(many=True)
	total = serializers.IntegerField()


class CreateReportResponseSerializer(serializers.Serializer):
	"""
	Serializer for create report response.
	"""
	success = serializers.BooleanField()
	report = DisasterReportSerializer(required=False)
	error = serializers.CharField(required=False)
