interface MobileNavToggleProps {
  active: boolean
  onToggle: () => void
}

export default function MobileNavToggle({ active, onToggle }: MobileNavToggleProps) {
  return (
    <button
      className={`mobile-nav-toggle${active ? ' active' : ''}`}
      onClick={onToggle}
      aria-label="Toggle navigation"
    >
      <div className="hamburger" />
    </button>
  )
}
