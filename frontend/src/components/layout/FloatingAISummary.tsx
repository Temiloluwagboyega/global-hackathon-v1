import { useState } from 'react'
import { Bot, X } from 'lucide-react'
import { Modal } from '../ui/Modal'
import { AISummary } from './AISummary'

export const FloatingAISummary = () => {
	const [isOpen, setIsOpen] = useState(false)

	return (
		<>
			{/* Floating Button */}
			<button
				onClick={() => setIsOpen(true)}
				className="fixed bottom-20 right-6 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 z-[9997]"
				aria-label="View AI Summary"
			>
				<Bot className="h-5 w-5" />
			</button>

			{/* Modal */}
			<Modal
				isOpen={isOpen}
				onClose={() => setIsOpen(false)}
				title="AI Summary"
				size="md"
			>
				<AISummary />
			</Modal>
		</>
	)
}
