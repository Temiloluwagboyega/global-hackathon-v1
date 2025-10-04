import { useState, useEffect, useCallback } from 'react'
import type { UserLocation } from '../../types'

interface GeolocationOptions {
	enableHighAccuracy?: boolean
	timeout?: number
	maximumAge?: number
}

interface GeolocationState {
	location: UserLocation | null
	error: string | null
	loading: boolean
	permission: 'granted' | 'denied' | 'prompt' | 'unknown'
}

const defaultOptions: GeolocationOptions = {
	enableHighAccuracy: true,
	timeout: 10000,
	maximumAge: 300000, // 5 minutes
}

export const useGeolocation = (options: GeolocationOptions = {}) => {
	const [state, setState] = useState<GeolocationState>({
		location: null,
		error: null,
		loading: false,
		permission: 'unknown',
	})

	const mergedOptions = { ...defaultOptions, ...options }

	const checkPermission = useCallback(async () => {
		if (!navigator.permissions) {
			setState(prev => ({ ...prev, permission: 'unknown' }))
			return
		}

		try {
			const permission = await navigator.permissions.query({ name: 'geolocation' as PermissionName })
			setState(prev => ({ ...prev, permission: permission.state as 'granted' | 'denied' | 'prompt' }))
		} catch (error) {
			setState(prev => ({ ...prev, permission: 'unknown' }))
		}
	}, [])

	const getCurrentPosition = useCallback(() => {
		if (!navigator.geolocation) {
			setState(prev => ({
				...prev,
				error: 'Geolocation is not supported by this browser',
				loading: false,
			}))
			return
		}

		setState(prev => ({ ...prev, loading: true, error: null }))

		navigator.geolocation.getCurrentPosition(
			(position) => {
				const location: UserLocation = {
					lat: position.coords.latitude,
					lng: position.coords.longitude,
					accuracy: position.coords.accuracy,
					timestamp: Date.now(),
				}

				setState(prev => ({
					...prev,
					location,
					loading: false,
					error: null,
					permission: 'granted',
				}))
			},
			(error) => {
				let errorMessage = 'Failed to get location'
				
				switch (error.code) {
					case error.PERMISSION_DENIED:
						errorMessage = 'Location access denied by user'
						setState(prev => ({ ...prev, permission: 'denied' }))
						break
					case error.POSITION_UNAVAILABLE:
						errorMessage = 'Location information is unavailable'
						break
					case error.TIMEOUT:
						errorMessage = 'Location request timed out'
						break
					default:
						errorMessage = 'An unknown error occurred'
						break
				}

				setState(prev => ({
					...prev,
					error: errorMessage,
					loading: false,
				}))
			},
			mergedOptions
		)
	}, [mergedOptions])

	const watchPosition = useCallback(() => {
		if (!navigator.geolocation) {
			setState(prev => ({
				...prev,
				error: 'Geolocation is not supported by this browser',
				loading: false,
			}))
			return () => {}
		}

		setState(prev => ({ ...prev, loading: true, error: null }))

		const watchId = navigator.geolocation.watchPosition(
			(position) => {
				const location: UserLocation = {
					lat: position.coords.latitude,
					lng: position.coords.longitude,
					accuracy: position.coords.accuracy,
					timestamp: Date.now(),
				}

				setState(prev => ({
					...prev,
					location,
					loading: false,
					error: null,
					permission: 'granted',
				}))
			},
			(error) => {
				let errorMessage = 'Failed to watch location'
				
				switch (error.code) {
					case error.PERMISSION_DENIED:
						errorMessage = 'Location access denied by user'
						setState(prev => ({ ...prev, permission: 'denied' }))
						break
					case error.POSITION_UNAVAILABLE:
						errorMessage = 'Location information is unavailable'
						break
					case error.TIMEOUT:
						errorMessage = 'Location request timed out'
						break
					default:
						errorMessage = 'An unknown error occurred'
						break
				}

				setState(prev => ({
					...prev,
					error: errorMessage,
					loading: false,
				}))
			},
			mergedOptions
		)

		return () => navigator.geolocation.clearWatch(watchId)
	}, [mergedOptions])

	useEffect(() => {
		checkPermission()
	}, [checkPermission])

	return {
		...state,
		getCurrentPosition,
		watchPosition,
		checkPermission,
	}
}
