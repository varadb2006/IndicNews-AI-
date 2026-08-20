export default function Footer() {
  return (
    <footer className="border-t border-wire-light bg-ink text-paper-bright/70">
      <div className="mx-auto max-w-6xl px-6 py-8 text-sm">
        <p className="font-body-en">
          IndicNews AI <span className="danda-divider mx-2">।</span>
          A Hindi news analysis desk, built on TF-IDF, FastText, and a
          multi-label classifier trained on real, deduplicated news data.
        </p>
      </div>
    </footer>
  )
}
