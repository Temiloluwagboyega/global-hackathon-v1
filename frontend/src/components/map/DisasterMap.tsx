import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import { Icon } from 'leaflet'
import L from 'leaflet'
import type { DisasterReport, Coordinates } from '../../types'
import { getDisasterEmoji, getDisasterDisplayName, formatTimestamp, formatDistance } from '../../utils'
import { cn } from '../../utils/cn'

// Fix for default markers in React Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
	iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
	iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

interface DisasterMapProps {
	reports: DisasterReport[]
	userLocation: Coordinates | null
	onMapClick?: (coordinates: Coordinates) => void
	selectedReport?: DisasterReport | null
	className?: string
}

// Custom marker icons for different disaster types
const createDisasterIcon = (type: DisasterReport['type']) => {
	const emoji = getDisasterEmoji(type)
	
	// Use encodeURIComponent to handle emoji characters
	const svgString = `
		<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
			<circle cx="16" cy="16" r="14" fill="white" stroke="#374151" stroke-width="2"/>
			<text x="16" y="20" text-anchor="middle" font-size="16" font-family="Arial, sans-serif">${emoji}</text>
		</svg>
	`
	
	return new Icon({
		iconUrl: `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgString)}`,
		iconSize: [32, 32],
		iconAnchor: [16, 16],
		popupAnchor: [0, -16],
	})
}

// Component to handle map click events
const MapClickHandler = ({ onMapClick }: { onMapClick?: (coordinates: Coordinates) => void }) => {
	useMapEvents({
		click: (e) => {
			if (onMapClick) {
				onMapClick({
					lat: e.latlng.lat,
					lng: e.latlng.lng,
				})
			}
		},
	})
	return null
}

export const DisasterMap = ({ 
	reports, 
	userLocation, 
	onMapClick, 
	selectedReport,
	className 
}: DisasterMapProps) => {
	const [mapCenter, setMapCenter] = useState<Coordinates>({ lat: 6.5244, lng: 3.3792 }) // Lagos default

	useEffect(() => {
		if (userLocation) {
			setMapCenter(userLocation)
		}
	}, [userLocation])

	useEffect(() => {
		if (selectedReport) {
			setMapCenter(selectedReport.location)
		}
	}, [selectedReport])

	const getMarkerColor = (type: DisasterReport['type']) => {
		const colors = {
			flood: 'text-blue-600',
			fire: 'text-red-600',
			accident: 'text-yellow-600',
			collapse: 'text-gray-600',
		}
		return colors[type]
	}

	const getStatusColor = (status: DisasterReport['status']) => {
		const colors = {
			active: 'text-red-600',
			resolved: 'text-green-600',
			investigating: 'text-yellow-600',
		}
		return colors[status]
	}

	return (
		<div className={cn('w-full h-full', className)}>
			<MapContainer
				center={mapCenter}
				zoom={13}
				className="w-full h-full"
				zoomControl={true}
			>
				<TileLayer
					attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
					url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
				/>
				
				{/* User location marker */}
				{userLocation && (
					<Marker
						position={[userLocation.lat, userLocation.lng]}
						icon={new Icon({
							iconUrl: `data:image/svg+xml;base64,${btoa(`
								<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
									<circle cx="12" cy="12" r="10" fill="#3b82f6" stroke="white" stroke-width="2"/>
									<circle cx="12" cy="12" r="4" fill="white"/>
								</svg>
							`)}`,
							iconSize: [24, 24],
							iconAnchor: [12, 12],
						})}
					>
						<Popup>
							<div className="text-center">
								<div className="font-semibold text-blue-600">Your Location</div>
								<div className="text-sm text-gray-600">
									{userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)}
								</div>
							</div>
						</Popup>
					</Marker>
				)}

				{/* Disaster report markers */}
				{reports.map((report) => (
					<Marker
						key={report.id}
						position={[report.location.lat, report.location.lng]}
						icon={createDisasterIcon(report.type)}
					>
						<Popup className="min-w-[250px]">
							<div className="space-y-2">
								<div className="flex items-center gap-2">
									<span className="text-lg">{getDisasterEmoji(report.type)}</span>
									<div>
										<h3 className="font-semibold text-gray-900">
											{getDisasterDisplayName(report.type)}
										</h3>
										<span className={cn('text-xs px-2 py-1 rounded-full', getStatusColor(report.status))}>
											{report.status}
										</span>
									</div>
								</div>
								
								<p className="text-sm text-gray-700">{report.description}</p>
								
								<div className="text-xs text-gray-500 space-y-1">
									<div>📍 {report.location.lat.toFixed(4)}, {report.location.lng.toFixed(4)}</div>
									<div>🕒 {formatTimestamp(report.timestamp)}</div>
									{userLocation && (
										<div>
											📏 {formatDistance(
												Math.sqrt(
													Math.pow(report.location.lat - userLocation.lat, 2) +
													Math.pow(report.location.lng - userLocation.lng, 2)
												) * 111 // Rough conversion to km
											)} away
										</div>
									)}
								</div>
								
								{report.imageUrl && (
									<div className="mt-2">
										<img 
											src={report.imageUrl} 
											alt="Disaster report" 
											className="w-full h-24 object-cover rounded"
										/>
									</div>
								)}
							</div>
						</Popup>
					</Marker>
				))}

				{/* Map click handler */}
				<MapClickHandler onMapClick={onMapClick} />
			</MapContainer>
		</div>
	)
}
