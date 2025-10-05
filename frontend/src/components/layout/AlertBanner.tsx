import { useState, useEffect } from 'react'
import { AlertTriangle, X, MapPin, CheckCircle, Clock } from 'lucide-react'
import { getDisasterEmoji, getDisasterDisplayName, formatDistance } from '../../utils'
import { useNearbyReports } from '../../hooks/utils/useDistance'
import { useReportUpdates } from '../../hooks/utils/useReportUpdates'
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
	type: 'new_report' | 'status_update'
	previousStatus?: string
}

export const AlertBanner = ({ userLocation, reports, onDismiss, className }: AlertBannerProps) => {
	const [alerts, setAlerts] = useState<AlertState[]>([])
	const [seenReportIds, setSeenReportIds] = useState<Set<string>>(new Set())
	const [seenUpdateIds, setSeenUpdateIds] = useState<Set<string>>(new Set())
	const nearbyReports = useNearbyReports(userLocation, reports, 5) // 5km radius
	const reportUpdates = useReportUpdates(reports)

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

	// Handle new reports
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
					type: 'new_report'
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

	// Handle status updates
	useEffect(() => {
		if (reportUpdates.length === 0) {
			return
		}

		// Filter for nearby reports with status updates
		const nearbyUpdates = reportUpdates.filter(update => {
			const report = reports.find(r => r.id === update.reportId)
			if (!report || !userLocation) return false
			
			// Check if report is within 5km
			const distance = Math.sqrt(
				Math.pow(report.location.lat - userLocation.lat, 2) +
				Math.pow(report.location.lng - userLocation.lng, 2)
			) * 111 // Rough conversion to km
			
			return distance <= 5 && !seenUpdateIds.has(update.reportId)
		})

		if (nearbyUpdates.length > 0) {
			const latestUpdate = nearbyUpdates[nearbyUpdates.length - 1]
			const report = reports.find(r => r.id === latestUpdate.reportId)
			
			if (report) {
				// Mark this update as seen
				setSeenUpdateIds(prev => new Set([...prev, latestUpdate.reportId]))
				
				const distance = userLocation ? Math.sqrt(
					Math.pow(report.location.lat - userLocation.lat, 2) +
					Math.pow(report.location.lng - userLocation.lng, 2)
				) * 111 : 0
				
				const statusUpdateAlert: AlertState = {
					id: `status-update-${latestUpdate.reportId}`,
					report: report,
					distance: distance,
					dismissed: false,
					type: 'status_update',
					previousStatus: latestUpdate.previousStatus
				}
				
				setAlerts(prev => [...prev, statusUpdateAlert])
				
				// Auto-dismiss after 5 seconds
				setTimeout(() => {
					dismissAlert(statusUpdateAlert.id)
				}, 5000)
			}
		}
	}, [reportUpdates, reports, userLocation, seenUpdateIds])

	const activeAlerts = alerts.filter(alert => !alert.dismissed)

	if (activeAlerts.length === 0) {
		return null
	}

	// Only show the most recent alert
	const currentAlert = activeAlerts[activeAlerts.length - 1]

	// Determine alert styling based on status
	const getAlertStyling = (alert: AlertState) => {
		// For new reports, use red (active status)
		// For status updates, use the report's current status color
		const status = alert.type === 'new_report' ? 'active' : alert.report.status
		
		switch (status) {
			case 'resolved':
				return {
					bgColor: 'bg-green-50',
					borderColor: 'border-green-200',
					iconColor: 'text-green-600',
					titleColor: 'text-green-800',
					textColor: 'text-green-700',
					icon: CheckCircle,
					title: 'Report Resolved'
				}
			case 'investigating':
				return {
					bgColor: 'bg-yellow-50',
					borderColor: 'border-yellow-200',
					iconColor: 'text-yellow-600',
					titleColor: 'text-yellow-800',
					textColor: 'text-yellow-700',
					icon: Clock,
					title: 'Under Investigation'
				}
			case 'active':
			default:
				return {
					bgColor: 'bg-red-50',
					borderColor: 'border-red-200',
					iconColor: 'text-red-600',
					titleColor: 'text-red-800',
					textColor: 'text-red-700',
					icon: AlertTriangle,
					title: alert.type === 'new_report' 
						? `${getDisasterDisplayName(alert.report.type)} Alert`
						: 'Report Active'
				}
		}
	}

	const styling = getAlertStyling(currentAlert)
	const IconComponent = styling.icon

	return (
		<div className={cn('fixed bottom-10 left-1/2 transform -translate-x-1/2 z-[9998] max-w-sm w-full px-4', className)}>
			<div
				className={cn(
					'text-nowrap border rounded-lg p-3 shadow-lg animate-in slide-in-from-bottom-2 duration-500',
					styling.bgColor,
					styling.borderColor
				)}
				role="alert"
			>
				<div className="flex items-center gap-2">
					<div className="flex-shrink-0">
						<IconComponent className={cn('h-4 w-4', styling.iconColor)} />
					</div>
					
					<div className="flex-1 min-w-0">
						<div className="flex items-center gap-2 mb-1">
							<span className="text-sm">{getDisasterEmoji(currentAlert.report.type)}</span>
							<h3 className={cn('text-xs font-semibold', styling.titleColor)}>
								{styling.title}
							</h3>
						</div>
						
						<p className={cn('text-xs mb-1 line-clamp-2', styling.textColor)}>
							{currentAlert.type === 'new_report' 
								? currentAlert.report.description
								: `${getDisasterDisplayName(currentAlert.report.type)} report status changed${
									currentAlert.previousStatus 
										? ` from ${currentAlert.previousStatus} to ${currentAlert.report.status}`
										: ` to ${currentAlert.report.status}`
								}`
							}
						</p>
						
						<div className="flex items-center gap-2 text-xs">
							<div className={cn('flex items-center gap-1', styling.textColor)}>
								<MapPin className="h-3 w-3" />
								<span>{formatDistance(currentAlert.distance)} away</span>
							</div>
						</div>
					</div>
					
					<button
						onClick={() => dismissAlert(currentAlert.id)}
						className={cn('flex-shrink-0 transition-colors', styling.textColor, 'hover:opacity-70')}
						aria-label="Dismiss alert"
					>
						<X className="h-3 w-3" />
					</button>
				</div>
			</div>
		</div>
	)
}
