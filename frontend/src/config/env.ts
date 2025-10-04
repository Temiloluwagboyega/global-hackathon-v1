// Environment configuration
export const config = {
	apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
	useMockData: false, // Always use real backend
	isDevelopment: import.meta.env.DEV,
	isProduction: import.meta.env.PROD,
}
