const LABELS = {
  word_count: 'Words',
  character_count: 'Characters',
  sentence_count: 'Sentences',
  estimated_reading_time_seconds: 'Reading time',
}

function formatValue(key, value) {
  if (key === 'estimated_reading_time_seconds') {
    return value < 60 ? `${value}s` : `${Math.round(value / 60)}m`
  }
  return value
}

export default function StatisticsPanel({ statistics }) {
  if (!statistics) return null

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {Object.entries(LABELS).map(([key, label]) => (
        <div
          key={key}
          className="rounded border border-wire-light bg-paper-bright px-4 py-3 text-center"
        >
          <p className="font-mono text-2xl text-ink">{formatValue(key, statistics[key])}</p>
          <p className="font-mono text-[0.65rem] uppercase tracking-[0.15em] text-wire">
            {label}
          </p>
        </div>
      ))}
    </div>
  )
}
