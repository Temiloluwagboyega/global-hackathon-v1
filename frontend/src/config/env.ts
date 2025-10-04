// Environment configuration
export const config = {
	apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001/api',
	useMockData: import.meta.env.VITE_USE_MOCK_DATA === 'true' || !import.meta.env.VITE_API_BASE_URL,
	isDevelopment: import.meta.env.DEV,
	isProduction: import.meta.env.PROD,
}
