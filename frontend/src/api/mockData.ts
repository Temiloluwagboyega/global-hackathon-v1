import type { DisasterReport, AISummary, DisasterType } from '../types'

// Mock disaster reports data
export const mockReports: DisasterReport[] = [
	{
		id: '1',
		type: 'flood',
		description: 'Heavy flooding in downtown area, water level rising rapidly',
		location: { lat: 6.5244, lng: 3.3792 }, // Lagos, Nigeria
		timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
		status: 'active',
		imageUrl: 'https://images.unsplash.com/photo-1574263867127-1c0b8b5b5b5b?w=400',
	},
	{
		id: '2',
		type: 'fire',
		description: 'Building fire reported in Victoria Island, smoke visible from distance',
		location: { lat: 6.4281, lng: 3.4219 },
		timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), // 4 hours ago
		status: 'investigating',
		imageUrl: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
	},
	{
		id: '3',
		type: 'accident',
		description: 'Multi-vehicle accident on Third Mainland Bridge causing traffic',
		location: { lat: 6.4654, lng: 3.4067 },
		timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(), // 1 hour ago
		status: 'active',
	},
	{
		id: '4',
		type: 'collapse',
		description: 'Partial building collapse in Surulere area, emergency services responding',
		location: { lat: 6.5018, lng: 3.3581 },
		timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(), // 6 hours ago
		status: 'investigating',
		imageUrl: 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=400',
	},
	{
		id: '5',
		type: 'flood',
		description: 'Flash flood in Ikoyi, roads impassable',
		location: { lat: 6.4474, lng: 3.4203 },
		timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(), // 3 hours ago
		status: 'active',
	},
	{
		id: '6',
		type: 'fire',
		description: 'Warehouse fire in Apapa port area',
		location: { lat: 6.4474, lng: 3.3603 },
		timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(), // 8 hours ago
		status: 'resolved',
	},
	{
		id: '7',
		type: 'accident',
		description: 'Pedestrian accident on Lagos-Ibadan expressway',
		location: { lat: 6.5244, lng: 3.3792 },
		timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30 minutes ago
		status: 'active',
	},
	{
		id: '8',
		type: 'collapse',
		description: 'Bridge structural damage reported in Lekki',
		location: { lat: 6.4698, lng: 3.5852 },
		timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(), // 12 hours ago
		status: 'investigating',
	},
]

export const mockAISummary: AISummary = {
	summary: 'In the last 24 hours: 3 floods, 2 fires, 2 accidents, and 1 building collapse reported in Lagos. Emergency services are actively responding to all incidents.',
	last24Hours: {
		floods: 3,
		fires: 2,
		accidents: 2,
		collapses: 1,
	},
	location: 'Lagos, Nigeria',
	generatedAt: new Date().toISOString(),
}

// Mock API delay simulation
export const mockDelay = (ms: number = 500) => 
	new Promise(resolve => setTimeout(resolve, ms))

// Generate a new mock report
export const generateMockReport = (type: DisasterType, location: { lat: number; lng: number }): DisasterReport => {
	const descriptions = {
		flood: [
			'Heavy flooding reported in the area',
			'Flash flood causing road closures',
			'Water level rising rapidly, evacuation recommended',
		],
		fire: [
			'Building fire with heavy smoke',
			'Warehouse fire spreading quickly',
			'Residential fire, emergency services responding',
		],
		accident: [
			'Multi-vehicle collision reported',
			'Pedestrian accident on main road',
			'Traffic accident causing delays',
		],
		collapse: [
			'Building structural damage reported',
			'Partial building collapse',
			'Bridge damage requiring immediate attention',
		],
	}

	const randomDescription = descriptions[type][Math.floor(Math.random() * descriptions[type].length)]
	
	return {
		id: Date.now().toString(),
		type,
		description: randomDescription,
		location,
		timestamp: new Date().toISOString(),
		status: 'active',
	}
}
