from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
	# Reports CRUD endpoints
	path('reports/', views.ReportsListView.as_view(), name='reports-list'),
	path('reports/<uuid:id>/', views.ReportDetailView.as_view(), name='report-detail'),
	path('reports/', views.CreateReportView.as_view(), name='create-report'),
	path('reports/<uuid:id>/status/', views.UpdateReportStatusView.as_view(), name='update-report-status'),
	
	# AI and summary endpoints
	path('ai/summary/', views.ai_summary_view, name='ai-summary'),
	path('summary/', views.reports_summary_view, name='reports-summary'),
	
	# Health check
	path('health/', views.health_check_view, name='health-check'),
]
