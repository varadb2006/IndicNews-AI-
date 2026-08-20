import { useState } from 'react'
import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Home' },
  { to: '/analyze', label: 'Analyze' },
  { to: '/features', label: 'Features' },
  { to: '/about', label: 'About' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <header className="border-b border-wire-light bg-ink text-paper-bright">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <NavLink to="/" className="flex items-baseline gap-2" onClick={() => setOpen(false)}>
          <span className="font-display-en text-xl font-semibold tracking-tight">
            IndicNews
          </span>
          <span className="hi-display text-xl text-marigold">AI</span>
        </NavLink>

        
        <nav className="hidden items-center gap-1 font-body-en text-sm sm:flex">
          {links.map((link, i) => (
            <span key={link.to} className="flex items-center">
              {i > 0 && <span className="danda-divider mx-2 text-wire">।</span>}
              <NavLink
                to={link.to}
                className={({ isActive }) =>
                  `rounded px-2 py-1 transition-colors ${
                    isActive
                      ? 'text-marigold'
                      : 'text-paper-bright/80 hover:text-paper-bright'
                  }`
                }
              >
                {link.label}
              </NavLink>
            </span>
          ))}
        </nav>

        
        <button
          type="button"
          onClick={() => setOpen(!open)}
          className="rounded p-2 text-paper-bright sm:hidden"
          aria-expanded={open}
          aria-label={open ? 'Close menu' : 'Open menu'}
        >
          <span className="hi-display text-2xl leading-none">{open ? '×' : '।।'}</span>
        </button>
      </div>

      
      {open && (
        <nav className="flex flex-col gap-1 border-t border-paper-bright/10 px-6 py-3 font-body-en text-sm sm:hidden">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `rounded px-2 py-2 transition-colors ${
                  isActive ? 'text-marigold' : 'text-paper-bright/80 hover:text-paper-bright'
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      )}
    </header>
  )
}
