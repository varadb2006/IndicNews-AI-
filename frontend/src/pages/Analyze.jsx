import { useNavigate } from 'react-router-dom'
import { useAnalyze } from '../hooks/useAnalyze'
import TextInputPanel from '../components/TextInputPanel'
import Spinner from '../components/Spinner'

export default function Analyze() {
  const { loading, error, runAnalysis } = useAnalyze()
  const navigate = useNavigate()

  async function handleSubmit(text) {
    try {
      const data = await runAnalysis(text)
      navigate('/results', { state: { result: data, sourceText: text } })
    } catch {
      
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.25em] text-marigold">
        The Desk
      </p>
      <h1 className="font-display-en mt-2 text-3xl font-semibold text-ink">
        Submit a dispatch for analysis
      </h1>
      <p className="mt-3 font-body-en text-wire">
        Paste a Hindi headline or a full article. Longer pieces (40+ words)
        also get an extractive summary.
      </p>

      <div className="mt-8">
        <TextInputPanel onSubmit={handleSubmit} loading={loading} />
      </div>

      {loading && <Spinner label="Reading the wire" />}

      {error && (
        <div className="mt-6 rounded border border-stamp bg-stamp/5 p-4 font-body-en text-sm text-stamp">
          {error}
        </div>
      )}
    </div>
  )
}
