from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
	# Reports CRUD endpoints
	path('reports/', views.ReportsListView.as_view(), name='reports-list'),
	path('reports/simple/', views.simple_reports_view, name='simple-reports'),
	path('reports/create/', views.CreateReportView.as_view(), name='create-report'),
	path('reports/<str:id>/', views.ReportDetailView.as_view(), name='report-detail'),
	path('reports/<str:id>/status/', views.UpdateReportStatusView.as_view(), name='update-report-status'),
	
	# AI and summary endpoints
	path('ai/summary/', views.ai_summary_view, name='ai-summary'),
	path('summary/', views.reports_summary_view, name='reports-summary'),
	
	# Reporter management
	path('reporter/id/', views.get_reporter_id_view, name='get-reporter-id'),
	path('reporter/simple/', views.simple_reporter_id_view, name='simple-reporter-id'),
	
	# Health check
	path('health/', views.health_check_view, name='health-check'),
]
