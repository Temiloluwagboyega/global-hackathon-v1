import { useState, useEffect } from 'react'
import { AlertTriangle, X, MapPin } from 'lucide-react'
import { getDisasterEmoji, getDisasterDisplayName, formatDistance } from '../../utils'
import { useNearbyReports } from '../../hooks/utils/useDistance'
import type { DisasterReport, UserLocation } from '../../types'
import { cn } from '../../utils/cn'

interface AlertBannerProps {
	userLocation: UserLocation | null
	reports: DisasterReport[]
	onDismiss?: (reportId: string) => void
	className?: string
}

interface AlertState {
	id: string
	report: DisasterReport
	distance: number
	dismissed: boolean
}

export const AlertBanner = ({ userLocation, reports, onDismiss, className }: AlertBannerProps) => {
	const [alerts, setAlerts] = useState<AlertState[]>([])
	const [seenReportIds, setSeenReportIds] = useState<Set<string>>(new Set())
	const nearbyReports = useNearbyReports(userLocation, reports, 5) // 5km radius

	const dismissAlert = (alertId: string) => {
		setAlerts(prev => 
			prev.map(alert => 
				alert.id === alertId 
					? { ...alert, dismissed: true }
					: alert
			)
		)
		onDismiss?.(alertId)
	}

	useEffect(() => {
		if (!userLocation || nearbyReports.length === 0) {
			return
		}

		// Only show alerts for NEW reports that haven't been seen before
		const newReports = nearbyReports.filter((report: any) => {
			const reportId = report.id || report.report?.id
			return reportId && !seenReportIds.has(reportId)
		})

		if (newReports.length > 0) {
			// Create alerts only for new reports
			const newAlerts: AlertState[] = newReports.map((report: any, index: number) => {
				const { distance, ...reportData } = report
				const reportId = reportData.id || `new-${index}`
				
				// Mark this report as seen
				setSeenReportIds(prev => new Set([...prev, reportId]))
				
				return {
					id: `alert-${reportId}`,
					report: reportData as DisasterReport,
					distance: distance || 0,
					dismissed: false,
				}
			})

			// Add new alerts (only show the most recent one)
			if (newAlerts.length > 0) {
				const latestAlert = newAlerts[newAlerts.length - 1] // Get the most recent
				setAlerts(prev => [...prev, latestAlert])
				
				// Auto-dismiss after 5 seconds
				setTimeout(() => {
					dismissAlert(latestAlert.id)
				}, 5000)
			}
		}
	}, [userLocation, nearbyReports, seenReportIds])

	const activeAlerts = alerts.filter(alert => !alert.dismissed)

	if (activeAlerts.length === 0) {
		return null
	}

	// Only show the most recent alert
	const currentAlert = activeAlerts[activeAlerts.length - 1]

	return (
		<div className={cn('fixed bottom-10 left-1/2 transform -translate-x-1/2 z-[9998] max-w-sm w-full px-4', className)}>
			<div
				className="bg-red-50 border border-red-200 rounded-lg p-3 shadow-lg animate-in slide-in-from-bottom-2 duration-500"
				role="alert"
			>
				<div className="flex items-center gap-2">
					<div className="flex-shrink-0">
						<AlertTriangle className="h-4 w-4 text-red-600" />
					</div>
					
					<div className="flex-1 min-w-0">
						<div className="flex items-center gap-2 mb-1">
							<span className="text-sm">{getDisasterEmoji(currentAlert.report.type)}</span>
							<h3 className="text-xs font-semibold text-red-800">
								{getDisasterDisplayName(currentAlert.report.type)} Alert
							</h3>
						</div>
						
						<p className="text-xs text-red-700 mb-1 line-clamp-2">
							{currentAlert.report.description}
						</p>
						
						<div className="flex items-center gap-2 text-xs text-red-600">
							<div className="flex items-center gap-1">
								<MapPin className="h-3 w-3" />
								<span>{formatDistance(currentAlert.distance)} away</span>
							</div>
						</div>
					</div>
					
					<button
						onClick={() => dismissAlert(currentAlert.id)}
						className="flex-shrink-0 text-red-400 hover:text-red-600 transition-colors"
						aria-label="Dismiss alert"
					>
						<X className="h-3 w-3" />
					</button>
				</div>
			</div>
		</div>
	)
}
