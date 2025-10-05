import { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents, useMap } from 'react-leaflet'
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
	center?: Coordinates
	zoom?: number
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

// Component to handle smooth map transitions
const MapTransitionHandler = ({ 
	center, 
	zoom = 15, 
	duration = 1000 
}: { 
	center?: Coordinates
	zoom?: number
	duration?: number
}) => {
	const map = useMap()
	const previousCenter = useRef<Coordinates | null>(null)

	useEffect(() => {
		if (center && map) {
			// Only animate if the center has actually changed
			if (!previousCenter.current || 
				previousCenter.current.lat !== center.lat || 
				previousCenter.current.lng !== center.lng) {
				
				// Smooth fly to the new location
				map.flyTo([center.lat, center.lng], zoom, {
					duration: duration / 1000, // Convert to seconds
					easeLinearity: 0.1,
				})
				
				previousCenter.current = center
			}
		}
	}, [center, zoom, duration, map])

	return null
}

export const DisasterMap = ({ 
	reports, 
	userLocation, 
	onMapClick, 
	selectedReport,
	center,
	zoom = 13,
	className 
}: DisasterMapProps) => {
	const [mapCenter, setMapCenter] = useState<Coordinates>(center || { lat: 6.5244, lng: 3.3792 }) // Lagos default
	
	// Debug user location in map component
	console.log('DisasterMap - userLocation:', userLocation)
	console.log('DisasterMap - center:', center)

	useEffect(() => {
		if (center) {
			setMapCenter(center)
		}
	}, [center])

	useEffect(() => {
		if (userLocation && !center) {
			setMapCenter(userLocation)
		}
	}, [userLocation, center])

	useEffect(() => {
		if (selectedReport && !center) {
			setMapCenter(selectedReport.location)
		}
	}, [selectedReport, center])


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
				zoom={zoom}
				className="w-full h-full"
				zoomControl={true}
			>
				<TileLayer
					attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
					url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
				/>
				
				{/* Map transition handler for smooth animations */}
				<MapTransitionHandler 
					center={center || selectedReport?.location} 
					zoom={center || selectedReport ? 15 : zoom}
					duration={1000}
				/>
				
				{/* User location marker */}
				{userLocation && (
					<Marker
						position={[userLocation.lat, userLocation.lng]}
						icon={new Icon({
							iconUrl: `data:image/svg+xml;base64,${btoa(`
								<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
									<circle cx="16" cy="16" r="14" fill="#3B82F6" stroke="white" stroke-width="3"/>
									<circle cx="16" cy="16" r="6" fill="white"/>
									<circle cx="16" cy="16" r="2" fill="#3B82F6"/>
								</svg>
							`)}`,
							iconSize: [32, 32],
							iconAnchor: [16, 16],
						})}
					>
						<Popup>
							<div className="text-center">
								<div className="font-semibold text-blue-600">📍 Your Location</div>
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
