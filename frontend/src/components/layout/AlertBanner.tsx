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
	const nearbyReports = useNearbyReports(userLocation, reports, 5) // 5km radius

	useEffect(() => {
		if (!userLocation || nearbyReports.length === 0) {
			setAlerts([])
			return
		}

		// Create alerts for nearby reports
		const newAlerts: AlertState[] = nearbyReports.map(report => ({
			id: `alert-${report.id}`,
			report: report as DisasterReport,
			distance: report.distance || 0,
			dismissed: false,
		}))

		// Filter out already dismissed alerts
		const existingAlertIds = alerts.filter(a => !a.dismissed).map(a => a.report.id)
		const filteredAlerts = newAlerts.filter(alert => !existingAlertIds.includes(alert.report.id))

		if (filteredAlerts.length > 0) {
			setAlerts(prev => [...prev, ...filteredAlerts])
		}
	}, [userLocation, nearbyReports])

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

	const activeAlerts = alerts.filter(alert => !alert.dismissed)

	if (activeAlerts.length === 0) {
		return null
	}

	return (
		<div className={cn('fixed top-4 left-4 right-4 z-[9998] space-y-2', className)}>
			{activeAlerts.map((alert) => (
				<div
					key={alert.id}
					className="bg-red-50 border border-red-200 rounded-lg p-4 shadow-lg animate-in slide-in-from-top-2 duration-300"
					role="alert"
				>
					<div className="flex items-start gap-3">
						<div className="flex-shrink-0">
							<AlertTriangle className="h-5 w-5 text-red-600" />
						</div>
						
						<div className="flex-1 min-w-0">
							<div className="flex items-center gap-2 mb-1">
								<span className="text-lg">{getDisasterEmoji(alert.report.type)}</span>
								<h3 className="text-sm font-semibold text-red-800">
									{getDisasterDisplayName(alert.report.type)} Alert
								</h3>
							</div>
							
							<p className="text-sm text-red-700 mb-2">
								{alert.report.description}
							</p>
							
							<div className="flex items-center gap-4 text-xs text-red-600">
								<div className="flex items-center gap-1">
									<MapPin className="h-3 w-3" />
									<span>{formatDistance(alert.distance)} away</span>
								</div>
								
								<div className="flex items-center gap-1">
									<span>📍 {alert.report.location.lat.toFixed(4)}, {alert.report.location.lng.toFixed(4)}</span>
								</div>
							</div>
						</div>
						
						<button
							onClick={() => dismissAlert(alert.id)}
							className="flex-shrink-0 text-red-400 hover:text-red-600 transition-colors"
							aria-label="Dismiss alert"
						>
							<X className="h-4 w-4" />
						</button>
					</div>
				</div>
			))}
		</div>
	)
}
