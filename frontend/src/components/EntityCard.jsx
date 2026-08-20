const TYPE_ORDER = ['Person', 'Location', 'Organization', 'Time', 'Number']

export default function EntityCard({ entities }) {
  const types = Object.keys(entities || {}).sort(
    (a, b) => TYPE_ORDER.indexOf(a) - TYPE_ORDER.indexOf(b)
  )

  if (types.length === 0) {
    return (
      <p className="font-body-en text-sm text-wire">
        No named entities found in this text.
      </p>
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {types.map((type) => (
        <div key={type} className="rounded border border-wire-light bg-paper-bright p-4">
          <p className="font-mono text-xs uppercase tracking-[0.15em] text-stamp">
            {type}
          </p>
          <ul className="hi-text mt-2 space-y-1 text-sm text-ink">
            {entities[type].map((name) => (
              <li key={name}>{name}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}
