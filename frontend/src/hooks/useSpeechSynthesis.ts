import { useState, useEffect, useCallback } from 'react'

export interface UseSpeechSynthesisReturn {
  speak: (text: string) => void
  cancel: () => void
  isSpeaking: boolean
  isSupported: boolean
}

/**
 * Accessible Text-To-Speech hook for Eduvia Learner Experience.
 *
 * Utilizes the standard Web Speech API with gentle pacing and pitch
 * tuned to Cognitive Calm principles.
 */
export function useSpeechSynthesis(): UseSpeechSynthesisReturn {
  const [isSpeaking, setIsSpeaking] = useState(false)
  const isSupported = typeof window !== 'undefined' && 'speechSynthesis' in window

  useEffect(() => {
    if (!isSupported) return

    const handleEnd = () => setIsSpeaking(false)
    const handleError = () => setIsSpeaking(false)

    window.speechSynthesis.addEventListener?.('end', handleEnd)
    window.speechSynthesis.addEventListener?.('error', handleError)

    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel()
      }
      window.speechSynthesis.removeEventListener?.('end', handleEnd)
      window.speechSynthesis.removeEventListener?.('error', handleError)
    }
  }, [isSupported])

  const cancel = useCallback(() => {
    if (isSupported && window.speechSynthesis) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
    }
  }, [isSupported])

  const speak = useCallback(
    (text: string) => {
      if (!isSupported || !window.speechSynthesis) return

      // Cancel any ongoing utterance
      window.speechSynthesis.cancel()

      if (!text || text.trim().length === 0) return

      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.88 // Gently measured, calm pacing
      utterance.pitch = 1.05 // Friendly, welcoming tone

      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      utterance.onerror = () => setIsSpeaking(false)

      window.speechSynthesis.speak(utterance)
    },
    [isSupported]
  )

  return { speak, cancel, isSpeaking, isSupported }
}
