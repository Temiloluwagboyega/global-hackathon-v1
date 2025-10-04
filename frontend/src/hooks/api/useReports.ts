import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { reportsApi } from '../../api/reports'
import type { CreateReportRequest } from '../../types'

// Query keys
export const queryKeys = {
	reports: ['reports'] as const,
	aiSummary: ['aiSummary'] as const,
}

// Hook to fetch all reports with polling
export const useReports = () => {
	return useQuery({
		queryKey: queryKeys.reports,
		queryFn: reportsApi.getReports,
		refetchInterval: 10000, // Poll every 10 seconds
		refetchIntervalInBackground: true,
		staleTime: 5000, // Consider data stale after 5 seconds
		gcTime: 5 * 60 * 1000, // Keep in cache for 5 minutes
		retry: 3,
		retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
	})
}

// Hook to create a new report
export const useCreateReport = () => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: (reportData: CreateReportRequest) => reportsApi.createReport(reportData),
		onSuccess: () => {
			// Invalidate and refetch reports
			queryClient.invalidateQueries({ queryKey: queryKeys.reports })
			// Also invalidate AI summary as it might change
			queryClient.invalidateQueries({ queryKey: queryKeys.aiSummary })
		},
		onError: (error) => {
			console.error('Failed to create report:', error)
		},
	})
}

// Hook to get AI summary
export const useAISummary = () => {
	return useQuery({
		queryKey: queryKeys.aiSummary,
		queryFn: reportsApi.getAISummary,
		refetchInterval: 5 * 60 * 1000, // Poll every 5 minutes
		staleTime: 2 * 60 * 1000, // Consider data stale after 2 minutes
		gcTime: 10 * 60 * 1000, // Keep in cache for 10 minutes
		retry: 2,
	})
}

// Hook to update report status
export const useUpdateReportStatus = () => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: ({ 
			reportId, 
			status 
		}: { 
			reportId: string
			status: 'active' | 'resolved' | 'investigating' 
		}) => reportsApi.updateReportStatus(reportId, status),
		onSuccess: () => {
			// Invalidate and refetch reports
			queryClient.invalidateQueries({ queryKey: queryKeys.reports })
		},
		onError: (error) => {
			console.error('Failed to update report status:', error)
		},
	})
}
