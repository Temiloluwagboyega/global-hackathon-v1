import { useState } from 'react'
import { Plus, X } from 'lucide-react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { Navbar } from '../../components/layout/Navbar'
import { DisasterMap } from '../../components/map/DisasterMap'
import { LiveFeed } from '../../components/layout/LiveFeed'
import { AlertBanner } from '../../components/layout/AlertBanner'
import { FloatingAISummary } from '../../components/layout/FloatingAISummary'
import { Modal } from '../../components/ui/Modal'
import { ReportForm } from '../../components/forms/ReportForm'
import { useReports } from '../../hooks/api/useReports'
import { useGeolocation } from '../../hooks/geolocation/useGeolocation'
import type { DisasterReport, Coordinates } from '../../types'

// Create a client
const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			staleTime: 5 * 60 * 1000, // 5 minutes
			gcTime: 10 * 60 * 1000, // 10 minutes
		},
	},
})

const MapPageContent = () => {
	const [showReportForm, setShowReportForm] = useState(false)
	const [selectedReport, setSelectedReport] = useState<DisasterReport | null>(null)
	const [selectedLocation, setSelectedLocation] = useState<Coordinates | null>(null)

	const { data: reportsData, isLoading } = useReports()
	const { location: userLocation, getCurrentPosition } = useGeolocation()

	const reports = reportsData?.reports || []

	const handleMapClick = (coordinates: Coordinates) => {
		setSelectedLocation(coordinates)
		setShowReportForm(true)
	}

	const handleReportClick = (report: DisasterReport) => {
		setSelectedReport(report)
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

				{/* Live Feed Sidebar */}
				<div className="w-80 border-l border-gray-200 bg-white">
					<LiveFeed
						userLocation={userLocation}
						onReportClick={handleReportClick}
						className="h-full"
					/>
				</div>
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

export const MapPage = () => {
	return (
		<QueryClientProvider client={queryClient}>
			<MapPageContent />
		</QueryClientProvider>
	)
}
