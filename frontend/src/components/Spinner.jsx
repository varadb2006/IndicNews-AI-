export default function Spinner({ label = 'Analyzing' }) {
  return (
    <div className="flex flex-col items-center gap-4 py-12" role="status" aria-live="polite">
      <div className="relative h-14 w-14">
        <div className="absolute inset-0 animate-spin rounded-full border-2 border-wire-light border-t-stamp" />
        <div className="absolute inset-0 flex items-center justify-center hi-display text-lg text-stamp">
          ।
        </div>
      </div>
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">
        {label}
        <span className="animate-pulse">…</span>
      </p>
    </div>
  )
}
