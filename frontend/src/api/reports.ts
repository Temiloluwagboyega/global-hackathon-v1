import { apiClient, handleApiError } from './client'
import { mockReports, mockDelay, generateMockReport } from './mockData'
import { config } from '../config/env'
import type { 
	DisasterReport,
	CreateReportRequest, 
	CreateReportResponse, 
	ReportsResponse,
	AISummary 
} from '../types'

// Check if we should use mock data
const USE_MOCK_DATA = config.useMockData

export const reportsApi = {
	// Get all reports
	getReports: async (): Promise<ReportsResponse> => {
		if (USE_MOCK_DATA) {
			await mockDelay(300)
			return {
				reports: mockReports.sort((a, b) => 
					new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
				),
				total: mockReports.length,
			}
		}

		try {
			const response = await apiClient.get<ReportsResponse>('/reports')
			return response.data
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Create a new report
	createReport: async (reportData: CreateReportRequest): Promise<CreateReportResponse> => {
		if (USE_MOCK_DATA) {
			await mockDelay(800)
			
			// Simulate occasional failures
			if (Math.random() < 0.1) {
				return {
					success: false,
					error: 'Failed to submit report. Please try again.',
				}
			}

			const newReport = generateMockReport(reportData.type, reportData.location)
			
			// Add to mock data
			mockReports.unshift(newReport)
			
			return {
				success: true,
				report: newReport,
			}
		}

		try {
			const formData = new FormData()
			formData.append('type', reportData.type)
			formData.append('description', reportData.description)
			formData.append('latitude', reportData.location.lat.toString())
			formData.append('longitude', reportData.location.lng.toString())
			
			if (reportData.imageFile) {
				formData.append('image', reportData.imageFile)
			}

			const response = await apiClient.post<CreateReportResponse>('/reports', formData, {
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
		if (USE_MOCK_DATA) {
			await mockDelay(1000)
			return {
				summary: 'In the last 24 hours: 3 floods, 2 fires, 2 accidents, and 1 building collapse reported in Lagos. Emergency services are actively responding to all incidents.',
				last24Hours: {
					floods: mockReports.filter(r => r.type === 'flood').length,
					fires: mockReports.filter(r => r.type === 'fire').length,
					accidents: mockReports.filter(r => r.type === 'accident').length,
					collapses: mockReports.filter(r => r.type === 'collapse').length,
				},
				location: 'Lagos, Nigeria',
				generatedAt: new Date().toISOString(),
			}
		}

		try {
			const response = await apiClient.get<AISummary>('/ai/summary')
			return response.data
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},

	// Update report status
	updateReportStatus: async (reportId: string, status: 'active' | 'resolved' | 'investigating'): Promise<void> => {
		if (USE_MOCK_DATA) {
			await mockDelay(500)
			const report = mockReports.find(r => r.id === reportId)
			if (report) {
				report.status = status
			}
			return
		}

		try {
			await apiClient.patch(`/reports/${reportId}/status`, { status })
		} catch (error) {
			throw new Error(handleApiError(error))
		}
	},
}
