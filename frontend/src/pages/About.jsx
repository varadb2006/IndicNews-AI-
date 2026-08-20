export default function About() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.25em] text-marigold">
        About
      </p>
      <h1 className="font-display-en mt-2 text-3xl font-semibold text-ink">
        Why this exists
      </h1>

      <div className="mt-8 space-y-6 font-body-en leading-relaxed text-ink">
        <p>
          Hindi is spoken by more than half a billion people, but the tools
          for processing Hindi text are nowhere near as mature as what
          exists for English. We ran into this directly: NLTK, one of the
          most commonly recommended NLP libraries, doesn&rsquo;t ship a
          Hindi stopword list at all &mdash; we checked, rather than
          assuming.
        </p>
        <p>
          This project is a working system built on a real dataset of
          Hindi news scraped from Inshorts &mdash; more than 185,000 rows.
          That number looked impressive until we deduplicated it. Only
          about 34,800 articles turned out to be genuinely unique; the rest
          were the same stories re-scraped on different days because they
          stayed on the homepage. Finding that early changed how every
          later stage was built, especially the similarity search below.
        </p>
        <p>
          The dataset also stores categories as a Python list, not a
          single label &mdash; a story can genuinely be both{' '}
          <span className="hi-text">sports</span> and{' '}
          <span className="hi-text">national</span> at once. Treating that
          as single-label classification would have thrown away real
          signal, so the classifier here is trained as multi-label from
          the start.
        </p>
        <p>
          A few specific bugs shaped the pipeline more than any single
          modeling decision did. IndicNLP&rsquo;s text normalizer quietly
          turns a plain colon into a Devanagari visarga character when it
          follows a Devanagari letter &mdash; corrupting punctuation like
          &ldquo;देखें:&rdquo; into something else entirely. scikit-learn&rsquo;s
          default tokenizer treats Hindi vowel signs as non-word
          characters, silently chopping words in half. Neither shows up in
          a training curve. Both would have quietly wrecked results if
          nobody had gone looking.
        </p>
        <p>
          The danda (।) you&rsquo;ll see used as a divider throughout this
          site isn&rsquo;t decoration &mdash; it&rsquo;s the exact
          character at the center of one of those bugs, kept visible as a
          small, honest nod to how this thing actually got built.
        </p>
      </div>
    </div>
  )
}
