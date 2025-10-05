from rest_framework import serializers
from mongoengine import Document
from .models import DisasterReport


class MongoEngineSerializer(serializers.Serializer):
	"""
	Base serializer for MongoEngine documents.
	"""
	def create(self, validated_data):
		model_class = self.Meta.model
		return model_class(**validated_data).save()
	
	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		return instance.save()


class DisasterReportSerializer(MongoEngineSerializer):
	"""
	Serializer for DisasterReport model.
	"""
	id = serializers.SerializerMethodField()  # Handle MongoDB ObjectId as string
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
	
	def get_id(self, obj):
		"""Return the MongoDB ObjectId as string."""
		# Use the custom mongodb_id property
		return obj.mongodb_id
	
	def get_image_url(self, obj):
		"""Return image URL if exists."""
		return obj.image_url
	
	def to_representation(self, instance):
		"""Customize the representation to match frontend expectations."""
		data = super().to_representation(instance)
		
		# Ensure all required fields are present
		data['description'] = instance.description
		data['status'] = instance.status
		data['reporterId'] = instance.reporter_id  # Explicitly add reporter_id
		
		# Map disaster_type to type for frontend compatibility
		data['type'] = instance.disaster_type
		
		# Map image_url to imageUrl for frontend compatibility
		if 'image_url' in data:
			data['imageUrl'] = data.pop('image_url')
		
		return data


class CreateDisasterReportSerializer(MongoEngineSerializer):
	"""
	Serializer for creating new disaster reports.
	"""
	latitude = serializers.FloatField(write_only=True)
	longitude = serializers.FloatField(write_only=True)
	type = serializers.CharField(source='disaster_type', write_only=True)
	description = serializers.CharField()
	reporter_id = serializers.CharField()
	image = serializers.ImageField(required=False, allow_null=True)
	timestamp = serializers.CharField(required=False, allow_null=True, write_only=True)
	
	class Meta:
		model = DisasterReport
		fields = [
			'type',
			'description',
			'latitude',
			'longitude',
			'image',
			'reporter_id',
			'timestamp',
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
	
	def create(self, validated_data):
		"""Create a new disaster report with image handling."""
		# Handle image file if provided
		image_file = validated_data.pop('image', None)
		image_url = None
		
		if image_file:
			try:
				# Upload to Cloudinary
				import cloudinary.uploader
				upload_result = cloudinary.uploader.upload(
					image_file,
					folder="disaster_reports",
					resource_type="image",
					transformation=[
						{"width": 800, "height": 600, "crop": "limit"},
						{"quality": "auto"},
						{"format": "auto"}
					]
				)
				image_url = upload_result['secure_url']
			except Exception as e:
				print(f"Cloudinary upload failed: {e}")
				# Fallback to placeholder if upload fails
				image_url = f"upload_failed_{image_file.name}"
		
		# Use provided timestamp or current time
		from django.utils import timezone
		from datetime import datetime
		
		timestamp_str = validated_data.pop('timestamp', None)
		print(f"=== TIMESTAMP DEBUG ===")
		print(f"Received timestamp from frontend: {timestamp_str}")
		print(f"Type: {type(timestamp_str)}")
		print(f"Validated data keys: {list(validated_data.keys())}")
		print(f"Current timezone.now(): {timezone.now()}")
		print(f"Current timezone.now().isoformat(): {timezone.now().isoformat()}")
		
		if timestamp_str:
			try:
				# Parse UTC timestamp and store as-is
				created_at = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
				print(f"Successfully parsed UTC timestamp: {created_at}")
				print(f"Created_at type: {type(created_at)}")
				print(f"Timezone info: {created_at.tzinfo}")
				print(f"Original timestamp string: {timestamp_str}")
			except (ValueError, AttributeError) as e:
				print(f"Failed to parse timestamp: {timestamp_str}, error: {e}, using current time")
				created_at = timezone.now()
		else:
			print("No timestamp provided, using current time")
			created_at = timezone.now()
		
		print(f"Final created_at: {created_at}")
		print(f"=== END TIMESTAMP DEBUG ===")
		
		# Create the report
		report = DisasterReport(
			disaster_type=validated_data['disaster_type'],
			description=validated_data['description'],
			latitude=validated_data['latitude'],
			longitude=validated_data['longitude'],
			reporter_id=validated_data['reporter_id'],
			image=image_url,
			status='active',
			created_at=created_at
		)
		
		return report.save()


class UpdateReportStatusSerializer(MongoEngineSerializer):
	"""
	Serializer for updating report status.
	"""
	status = serializers.CharField()
	
	class Meta:
		model = DisasterReport
		fields = ['status']
	
	def validate_status(self, value):
		"""Validate status is valid."""
		valid_statuses = [choice[0] for choice in DisasterReport.STATUS_CHOICES]
		if value not in valid_statuses:
			raise serializers.ValidationError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
		return value
	
	def update(self, instance, validated_data):
		"""Update the instance with validated data."""
		instance.status = validated_data.get('status', instance.status)
		instance.save()
		return instance


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
