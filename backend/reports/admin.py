from django.contrib import admin
from .models import DisasterReport


@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'disaster_type',
		'description_short',
		'latitude',
		'longitude',
		'status',
		'created_at',
		'updated_at',
	]
	list_filter = [
		'disaster_type',
		'status',
		'created_at',
	]
	search_fields = [
		'description',
		'reporter_id',
	]
	readonly_fields = [
		'id',
		'created_at',
		'updated_at',
	]
	ordering = ['-created_at']
	
	def description_short(self, obj):
		"""Return truncated description for list view."""
		return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
	description_short.short_description = 'Description'