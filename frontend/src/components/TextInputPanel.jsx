import { useState } from 'react'

const EXAMPLES = [
  { label: 'sports', text: 'भारतीय क्रिकेट टीम ने आज मैच में शानदार जीत दर्ज की' },
  { label: 'business', text: 'शेयर बाजार में आज तेजी देखी गई और सेंसेक्स नए रिकॉर्ड पर पहुंचा' },
  { label: 'politics', text: 'प्रधानमंत्री ने आज नई शिक्षा नीति पर बैठक की अध्यक्षता की' },
]

export default function TextInputPanel({ onSubmit, loading }) {
  const [text, setText] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (!text.trim() || loading) return
    onSubmit(text.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <label htmlFor="analyze-input" className="sr-only">
        Hindi headline or article
      </label>
      <textarea
        id="analyze-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="एक हिंदी समाचार शीर्षक या पूरा लेख यहाँ पेस्ट करें…"
        rows={8}
        className="hi-text w-full resize-y rounded border-2 border-ink bg-paper-bright p-4 text-lg leading-relaxed text-ink placeholder:text-wire focus:border-stamp focus:outline-none"
      />

      <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3 font-mono text-xs text-wire">
          <span className="uppercase tracking-[0.1em]">Try:</span>
          {EXAMPLES.map((example, i) => (
            <span key={example.label} className="flex items-center gap-3">
              {i > 0 && <span className="danda-divider">।</span>}
              <button
                type="button"
                onClick={() => setText(example.text)}
                className="underline decoration-dotted underline-offset-4 hover:text-stamp"
              >
                {example.label}
              </button>
            </span>
          ))}
        </div>

        <button
          type="submit"
          disabled={!text.trim() || loading}
          className="rounded bg-stamp px-6 py-2.5 font-display-en font-semibold text-paper-bright transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>
      </div>
    </form>
  )
}
