// Environment configuration
export const config = {
	apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 
		(import.meta.env.PROD 
			? 'https://disaster-report-map.onrender.com/api' 
			: 'http://localhost:8001/api'),
	useMockData: false, // Always use real backend
	isDevelopment: import.meta.env.DEV,
	isProduction: import.meta.env.PROD,
}
