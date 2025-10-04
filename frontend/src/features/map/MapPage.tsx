import { useState } from 'react'
import { Plus } from 'lucide-react'
import { Toaster } from 'react-hot-toast'
import { Navbar } from '../../components/layout/Navbar'
import { DisasterMap } from '../../components/map/DisasterMap'
import { ResponsiveLiveFeed } from '../../components/layout/ResponsiveLiveFeed'
import { AlertBanner } from '../../components/layout/AlertBanner'
import { FloatingAISummary } from '../../components/layout/FloatingAISummary'
import { Modal } from '../../components/ui/Modal'
import { ReportForm } from '../../components/forms/ReportForm'
import { useReports, useReporterId, useHealthCheck } from '../../hooks/api/useReports'
import { useGeolocation } from '../../hooks/geolocation/useGeolocation'
import type { DisasterReport, Coordinates } from '../../types'

const MapPage = () => {
	const [showReportForm, setShowReportForm] = useState(false)
	const [selectedReport, setSelectedReport] = useState<DisasterReport | null>(null)
	const [selectedLocation, setSelectedLocation] = useState<Coordinates | null>(null)
	const [mapCenter, setMapCenter] = useState<Coordinates>({ lat: 6.5244, lng: 3.3792 }) // Lagos default

	const { data: reportsData } = useReports()
	const { data: reporterIdData } = useReporterId()
	const { data: healthData } = useHealthCheck()
	const { location: userLocation, getCurrentPosition } = useGeolocation()

	const reports = reportsData?.reports || []

	const handleMapClick = (coordinates: Coordinates) => {
		setSelectedLocation(coordinates)
		setShowReportForm(true)
	}

	const handleReportClick = (report: DisasterReport) => {
		setSelectedReport(report)
		// Center map on the selected report
		setMapCenter(report.location)
	}

	const handleReportSuccess = () => {
		setShowReportForm(false)
		setSelectedLocation(null)
	}

	const handleReportCancel = () => {
		setShowReportForm(false)
		setSelectedLocation(null)
	}

	return (
		<div className="h-screen flex flex-col bg-gray-50">
			{/* Navbar */}
			<Navbar />

			{/* Main Content */}
			<div className="flex-1 flex overflow-hidden">
				{/* Map */}
				<div className="flex-1 relative">
					<DisasterMap
						reports={reports}
						userLocation={userLocation}
						onMapClick={handleMapClick}
						selectedReport={selectedReport}
						center={mapCenter}
						className="h-full"
					/>

					{/* Floating Report Button */}
					<button
						onClick={() => setShowReportForm(true)}
						className="absolute bottom-6 right-6 bg-primary-600 hover:bg-primary-700 text-white p-4 rounded-full shadow-lg transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 z-[9997]"
						aria-label="Report disaster"
					>
						<Plus className="h-6 w-6" />
					</button>
				</div>

				{/* Responsive Live Feed Sidebar */}
				<ResponsiveLiveFeed
					userLocation={userLocation}
					onReportClick={handleReportClick}
					className="h-full"
				/>
			</div>

			{/* Alert Banner */}
			<AlertBanner
				userLocation={userLocation}
				reports={reports}
			/>

			{/* Floating AI Summary Button */}
			<FloatingAISummary />

			{/* Report Form Modal */}
			<Modal
				isOpen={showReportForm}
				onClose={handleReportCancel}
				title="Report Disaster"
				size="lg"
			>
				<ReportForm
					onSuccess={handleReportSuccess}
					onCancel={handleReportCancel}
					initialLocation={selectedLocation}
				/>
			</Modal>

			{/* Toast Notifications */}
			<Toaster
				position="top-right"
				toastOptions={{
					duration: 4000,
					style: {
						background: '#363636',
						color: '#fff',
					},
					success: {
						duration: 3000,
						iconTheme: {
							primary: '#10b981',
							secondary: '#fff',
						},
					},
					error: {
						duration: 5000,
						iconTheme: {
							primary: '#ef4444',
							secondary: '#fff',
						},
					},
				}}
			/>
		</div>
	)
}

export { MapPage }
