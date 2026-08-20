import { useState, useCallback } from 'react'
import { analyzeText } from '../services/api'


export function useAnalyze() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runAnalysis = useCallback(async (text) => {
    setLoading(true)
    setError(null)
    try {
      const data = await analyzeText(text)
      setResult(data)
      return data
    } catch (err) {
      const message =
        err.response?.data?.error ||
        (err.code === 'ECONNABORTED'
          ? 'The request took too long to respond. The server may still be starting up (Stanza\u2019s pipeline load is slow) -- try again in a moment.'
          : 'Could not reach the analysis server. Check that the Flask backend is running.')
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  return { result, loading, error, runAnalysis, setResult }
}
