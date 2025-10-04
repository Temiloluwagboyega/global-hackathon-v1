import math
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from django.db.models import Q, Count
from .models import DisasterReport
from .serializers import (
	DisasterReportSerializer,
	CreateDisasterReportSerializer,
	UpdateReportStatusSerializer,
	AISummarySerializer,
	ReportsResponseSerializer,
	CreateReportResponseSerializer,
)


def haversine_distance(lat1, lon1, lat2, lon2):
	"""
	Calculate the great circle distance between two points on Earth (in kilometers).
	"""
	# Convert decimal degrees to radians
	lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
	
	# Haversine formula
	dlat = lat2 - lat1
	dlon = lon2 - lon1
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a))
	
	# Radius of earth in kilometers
	r = 6371
	return c * r


class CustomPagination(PageNumberPagination):
	page_size = 50
	page_size_query_param = 'page_size'
	max_page_size = 100


class ReportsListView(ListAPIView):
	"""
	API view to list disaster reports with optional location filtering.
	"""
	serializer_class = DisasterReportSerializer
	pagination_class = CustomPagination
	permission_classes = [AllowAny]
	
	def get_queryset(self):
		queryset = DisasterReport.objects.all()
		
		# Get query parameters
		lat = self.request.query_params.get('lat')
		lng = self.request.query_params.get('lng')
		radius = float(self.request.query_params.get('radius', 10))  # Default 10km
		
		# If lat/lng provided, filter by radius
		if lat and lng:
			try:
				lat = float(lat)
				lng = float(lng)
				
				# Filter reports within radius
				filtered_reports = []
				for report in queryset:
					distance = haversine_distance(lat, lng, report.latitude, report.longitude)
					if distance <= radius:
						filtered_reports.append(report)
				
				# Convert back to queryset-like object
				queryset = DisasterReport.objects.filter(
					id__in=[report.id for report in filtered_reports]
				)
				
			except (ValueError, TypeError):
				# If invalid coordinates, return all reports
				pass
		
		return queryset


class ReportDetailView(RetrieveAPIView):
	"""
	API view to retrieve a single disaster report.
	"""
	queryset = DisasterReport.objects.all()
	serializer_class = DisasterReportSerializer
	permission_classes = [AllowAny]
	lookup_field = 'id'


class CreateReportView(CreateAPIView):
	"""
	API view to create a new disaster report.
	"""
	queryset = DisasterReport.objects.all()
	serializer_class = CreateDisasterReportSerializer
	permission_classes = [AllowAny]
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			report = serializer.save()
			response_serializer = DisasterReportSerializer(report)
			
			response_data = {
				'success': True,
				'report': response_serializer.data
			}
			
			return Response(response_data, status=status.HTTP_201_CREATED)
		
		response_data = {
			'success': False,
			'error': 'Failed to create report. Please check your data.'
		}
		
		return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UpdateReportStatusView(UpdateAPIView):
	"""
	API view to update report status.
	"""
	queryset = DisasterReport.objects.all()
	serializer_class = UpdateReportStatusSerializer
	permission_classes = [AllowAny]
	lookup_field = 'id'
	
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		
		if serializer.is_valid():
			serializer.save()
			return Response({'success': True}, status=status.HTTP_200_OK)
		
		return Response({'success': False, 'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def ai_summary_view(request):
	"""
	API view to get AI summary of reports in the last 24 hours.
	"""
	try:
		# Get reports from last 24 hours
		last_24_hours = timezone.now() - timedelta(hours=24)
		recent_reports = DisasterReport.objects.filter(created_at__gte=last_24_hours)
		
		# Count by disaster type
		summary_counts = {
			'floods': recent_reports.filter(disaster_type='flood').count(),
			'fires': recent_reports.filter(disaster_type='fire').count(),
			'accidents': recent_reports.filter(disaster_type='accident').count(),
			'collapses': recent_reports.filter(disaster_type='collapse').count(),
		}
		
		# Generate summary text
		total_reports = sum(summary_counts.values())
		if total_reports == 0:
			summary_text = "No disaster reports in the last 24 hours."
		else:
			summary_parts = []
			for disaster_type, count in summary_counts.items():
				if count > 0:
					summary_parts.append(f"{count} {disaster_type}")
			
			summary_text = f"In the last 24 hours: {', '.join(summary_parts)} reported. Emergency services are actively responding to all incidents."
		
		# Create response data
		response_data = {
			'summary': summary_text,
			'last24Hours': summary_counts,
			'location': 'Global',  # Could be made dynamic based on user location
			'generatedAt': timezone.now().isoformat(),
		}
		
		return Response(response_data, status=status.HTTP_200_OK)
		
	except Exception as e:
		return Response(
			{'error': 'Failed to generate AI summary'},
			status=status.HTTP_500_INTERNAL_SERVER_ERROR
		)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_view(request):
	"""
	Simple health check endpoint.
	"""
	return JsonResponse({
		'status': 'healthy',
		'timestamp': timezone.now().isoformat(),
		'service': 'Disaster Response API'
	})


@api_view(['GET'])
@permission_classes([AllowAny])
def reports_summary_view(request):
	"""
	API view to get a summary of all reports (alternative to AI summary).
	"""
	try:
		# Get all reports
		all_reports = DisasterReport.objects.all()
		
		# Count by disaster type
		summary_counts = {
			'floods': all_reports.filter(disaster_type='flood').count(),
			'fires': all_reports.filter(disaster_type='fire').count(),
			'accidents': all_reports.filter(disaster_type='accident').count(),
			'collapses': all_reports.filter(disaster_type='collapse').count(),
		}
		
		# Count by status
		status_counts = {
			'active': all_reports.filter(status='active').count(),
			'resolved': all_reports.filter(status='resolved').count(),
			'investigating': all_reports.filter(status='investigating').count(),
		}
		
		response_data = {
			'total_reports': all_reports.count(),
			'by_type': summary_counts,
			'by_status': status_counts,
			'last_updated': timezone.now().isoformat(),
		}
		
		return Response(response_data, status=status.HTTP_200_OK)
		
	except Exception as e:
		return Response(
			{'error': 'Failed to generate summary'},
			status=status.HTTP_500_INTERNAL_SERVER_ERROR
		)