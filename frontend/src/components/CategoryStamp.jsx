
export default function CategoryStamp({ label, confidence, index = 0 }) {
  
  const rotation = index % 2 === 0 ? '-rotate-6' : 'rotate-3'

  return (
    <div
      className={`inline-flex flex-col items-center justify-center rounded-full border-[3px] border-double border-stamp px-5 py-4 text-stamp ${rotation}`}
      style={{ minWidth: '7.5rem' }}
    >
      <span className="font-display-en text-sm font-semibold uppercase tracking-wide">
        {label}
      </span>
      <span className="font-mono text-xs opacity-80">{confidence}%</span>
    </div>
  )
}
