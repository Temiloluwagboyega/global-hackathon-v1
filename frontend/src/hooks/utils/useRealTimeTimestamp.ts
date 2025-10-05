import { useState, useEffect } from 'react'
import { formatTimestamp } from '../../utils'

/**
 * Hook to get real-time formatted timestamp that updates every minute
 */
export const useRealTimeTimestamp = (timestamp: string): string => {
	const [formattedTime, setFormattedTime] = useState(() => formatTimestamp(timestamp))
	const [lastUpdate, setLastUpdate] = useState(Date.now())

	useEffect(() => {
		// Update immediately when timestamp changes
		setFormattedTime(formatTimestamp(timestamp))
		setLastUpdate(Date.now())

		// Set up interval to update every minute
		const interval = setInterval(() => {
			setFormattedTime(formatTimestamp(timestamp))
			setLastUpdate(Date.now())
		}, 60000) // Update every minute

		return () => clearInterval(interval)
	}, [timestamp])

	return formattedTime
}
