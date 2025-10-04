import { apiClient, handleApiError } from './client'
import type { 
	DisasterReport,
	CreateReportRequest, 
	CreateReportResponse, 
	ReportsResponse,
	AISummary 
} from '../types'

export const reportsApi = {
	// Get all reports
	getReports: async (): Promise<ReportsResponse> => {
		try {
			const response = await apiClient.get('/reports/')
			// Transform the response to match our frontend expectations
			const data = response.data
			return {
				reports: data.results || [],
				total: data.count || 0,
			}
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Create a new report
	createReport: async (reportData: CreateReportRequest): Promise<CreateReportResponse> => {
		try {
			// Prepare FormData for multipart upload (to support images)
			const formData = new FormData()
			formData.append('type', reportData.type)
			formData.append('description', reportData.description)
			formData.append('latitude', reportData.location.lat.toString())
			formData.append('longitude', reportData.location.lng.toString())
			formData.append('status', 'active')
			
			// Add image if provided
			if (reportData.imageFile) {
				formData.append('image', reportData.imageFile)
			}

			const response = await apiClient.post<CreateReportResponse>('/reports/create/', formData, {
				headers: {
					'Content-Type': 'multipart/form-data',
				},
			})
			return response.data
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Get AI summary
	getAISummary: async (): Promise<AISummary> => {
		try {
			const response = await apiClient.get<AISummary>('/ai/summary/')
			return response.data
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Update report status
	updateReportStatus: async (reportId: string, status: 'active' | 'resolved' | 'investigating'): Promise<void> => {
		try {
			await apiClient.patch(`/reports/${reportId}/status/`, { status })
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Get reporter ID (session-based)
	getReporterId: async (): Promise<{ reporter_id: string; session_active: boolean; timestamp: string }> => {
		try {
			const response = await apiClient.get('/reporter/id/')
			return response.data
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Health check
	healthCheck: async (): Promise<{ status: string; timestamp: string; service: string }> => {
		try {
			const response = await apiClient.get('/health/')
			return response.data
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},
}
