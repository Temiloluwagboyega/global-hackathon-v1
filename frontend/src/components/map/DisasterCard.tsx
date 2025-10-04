import { MapPin, Clock, Eye } from 'lucide-react'
import { cn } from '../../utils/cn'
import { getDisasterEmoji, getDisasterDisplayName, getStatusColor, formatTimestamp, formatDistance } from '../../utils'
import type { DisasterReport } from '../../types'

interface DisasterCardProps {
	report: DisasterReport
	userLocation?: { lat: number; lng: number } | null
	onClick?: () => void
	className?: string
}

export const DisasterCard = ({ report, userLocation, onClick, className }: DisasterCardProps) => {
	const distance = userLocation ? 
		Math.sqrt(
			Math.pow(report.location.lat - userLocation.lat, 2) +
			Math.pow(report.location.lng - userLocation.lng, 2)
		) * 111 // Rough conversion to km
		: null

	return (
		<div
			onClick={onClick}
			className={cn(
				'bg-white border border-gray-200 rounded-lg p-4 cursor-pointer hover:shadow-md transition-shadow',
				className
			)}
		>
			{/* Header */}
			<div className="flex items-start justify-between mb-3">
				<div className="flex items-center gap-2">
					<span className="text-lg">{getDisasterEmoji(report.type)}</span>
					<div>
						<h3 className="font-semibold text-gray-900 text-sm">
							{getDisasterDisplayName(report.type)}
						</h3>
						<span className={cn('text-xs px-2 py-1 rounded-full', getStatusColor(report.status))}>
							{report.status}
						</span>
					</div>
				</div>
				
				{onClick && (
					<Eye className="h-4 w-4 text-gray-400" />
				)}
			</div>

			{/* Description */}
			<p className="text-sm text-gray-700 mb-3 line-clamp-2">
				{report.description}
			</p>

			{/* Image */}
			{report.imageUrl && (
				<div className="mb-3">
					<img
						src={report.imageUrl}
						alt="Disaster report"
						className="w-full h-20 object-cover rounded"
					/>
				</div>
			)}

			{/* Footer */}
			<div className="flex items-center justify-between text-xs text-gray-500">
				<div className="flex items-center gap-1">
					<Clock className="h-3 w-3" />
					<span>{formatTimestamp(report.timestamp)}</span>
				</div>
				
				{userLocation && distance !== null && (
					<div className="flex items-center gap-1">
						<MapPin className="h-3 w-3" />
						<span>{formatDistance(distance)}</span>
					</div>
				)}
			</div>
		</div>
	)
}
