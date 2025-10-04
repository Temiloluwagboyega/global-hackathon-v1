import { MapPin, AlertTriangle, Car, Building } from 'lucide-react'
import { getDisasterDisplayName } from '../../utils'
import type { DisasterType } from '../../types'

interface NavbarProps {
	className?: string
}

const disasterTypes: { type: DisasterType; icon: React.ReactNode }[] = [
	{ type: 'flood', icon: '🌊' },
	{ type: 'fire', icon: '🔥' },
	{ type: 'accident', icon: '🚑' },
	{ type: 'collapse', icon: '🏚️' },
]

export const Navbar = ({ className }: NavbarProps) => {
	return (
		<nav className={`bg-white border-b border-gray-200 px-4 py-3 ${className}`}>
			<div className="flex items-center justify-between">
				{/* Logo and Title */}
				<div className="flex items-center gap-3">
					<div className="flex items-center gap-2">
						<MapPin className="h-6 w-6 text-gray-800" />
						<h1 className="text-xl font-bold text-gray-900">
							Disaster Response Map
						</h1>
					</div>
				</div>

				{/* Legend */}
				<div className="hidden md:flex items-center gap-4">
					<span className="text-sm text-gray-600 font-medium">Legend:</span>
					<div className="flex items-center gap-3">
						{disasterTypes.map(({ type, icon }) => (
							<div key={type} className="flex items-center gap-1">
								<span className="text-sm">{icon}</span>
								<span className="text-xs text-gray-600">
									{getDisasterDisplayName(type)}
								</span>
							</div>
						))}
					</div>
				</div>

				{/* Status Indicator */}
				<div className="flex items-center gap-2">
					<div className="flex items-center gap-1 text-sm text-green-600">
						<div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
						<span className="hidden sm:inline">Live</span>
					</div>
				</div>
			</div>

			{/* Mobile Legend */}
			<div className="md:hidden mt-3 pt-3 border-t border-gray-200">
				<div className="flex items-center gap-4 overflow-x-auto">
					<span className="text-sm text-gray-600 font-medium whitespace-nowrap">Legend:</span>
					<div className="flex items-center gap-3">
						{disasterTypes.map(({ type, icon }) => (
							<div key={type} className="flex items-center gap-1 whitespace-nowrap">
								<span className="text-sm">{icon}</span>
								<span className="text-xs text-gray-600">
									{getDisasterDisplayName(type)}
								</span>
							</div>
						))}
					</div>
				</div>
			</div>
		</nav>
	)
}
