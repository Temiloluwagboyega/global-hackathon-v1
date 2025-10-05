import { useState, useEffect } from 'react'
import { reportsApi } from '../../api/reports'

interface WelcomeModalState {
	shouldShow: boolean
	isLoading: boolean
	error: string | null
}

export const useWelcomeModal = () => {
	const [state, setState] = useState<WelcomeModalState>({
		shouldShow: false,
		isLoading: true,
		error: null,
	})

	const checkWelcomeModalStatus = async () => {
		try {
			setState(prev => ({ ...prev, isLoading: true, error: null }))
			
			const response = await reportsApi.checkWelcomeModalViewed()
			
			setState({
				shouldShow: !response.has_viewed,
				isLoading: false,
				error: null,
			})
		} catch (error) {
			console.error('Failed to check welcome modal status:', error)
			setState({
				shouldShow: true, // Show by default if check fails
				isLoading: false,
				error: error instanceof Error ? error.message : 'Failed to check welcome modal status',
			})
		}
	}

	const markWelcomeModalViewed = async () => {
		try {
			await reportsApi.markWelcomeModalViewed()
			setState(prev => ({ ...prev, shouldShow: false }))
		} catch (error) {
			console.error('Failed to mark welcome modal as viewed:', error)
			// Still hide the modal even if marking fails
			setState(prev => ({ ...prev, shouldShow: false }))
		}
	}

	const hideWelcomeModal = () => {
		setState(prev => ({ ...prev, shouldShow: false }))
	}

	// Check welcome modal status on mount
	useEffect(() => {
		checkWelcomeModalStatus()
	}, [])

	return {
		shouldShow: state.shouldShow,
		isLoading: state.isLoading,
		error: state.error,
		markWelcomeModalViewed,
		hideWelcomeModal,
		refetch: checkWelcomeModalStatus,
	}
}
