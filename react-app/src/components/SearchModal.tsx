import { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { search, type SearchResult } from '../utils/searchIndex'

interface SearchModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function SearchModal({ isOpen, onClose }: SearchModalProps) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [selectedIndex, setSelectedIndex] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setQuery('')
      setResults([])
      setSelectedIndex(0)
      // Small delay to ensure modal is rendered
      setTimeout(() => inputRef.current?.focus(), 50)
    }
  }, [isOpen])

  // Search as you type
  useEffect(() => {
    const results = search(query)
    setResults(results)
    setSelectedIndex(0)
  }, [query])

  const goToResult = useCallback((result: SearchResult) => {
    navigate(result.url)
    onClose()
  }, [navigate, onClose])

  // Keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setSelectedIndex(i => Math.min(i + 1, results.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setSelectedIndex(i => Math.max(i - 1, 0))
        break
      case 'Enter':
        e.preventDefault()
        if (results[selectedIndex]) {
          goToResult(results[selectedIndex])
        }
        break
      case 'Escape':
        onClose()
        break
    }
  }, [results, selectedIndex, goToResult, onClose])

  // Close on backdrop click
  const handleBackdropClick = useCallback((e: React.MouseEvent) => {
    if (e.target === e.currentTarget) onClose()
  }, [onClose])

  if (!isOpen) return null

  return (
    <div className="search-modal__backdrop" onClick={handleBackdropClick}>
      <div className="search-modal">
        <div className="search-modal__header">
          <svg className="search-modal__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            className="search-modal__input"
            placeholder="Search pages..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <kbd className="search-modal__kbd">ESC</kbd>
        </div>

        {results.length > 0 && (
          <ul className="search-modal__results">
            {results.map((result, i) => (
              <li key={result.url}>
                <button
                  className={`search-modal__result${i === selectedIndex ? ' search-modal__result--selected' : ''}`}
                  onClick={() => goToResult(result)}
                  onMouseEnter={() => setSelectedIndex(i)}
                >
                  <span className="search-modal__result-title">{result.title}</span>
                  <span className="search-modal__result-snippet">{result.snippet}</span>
                </button>
              </li>
            ))}
          </ul>
        )}

        {query.length >= 2 && results.length === 0 && (
          <div className="search-modal__empty">
            No results for "{query}"
          </div>
        )}

        <div className="search-modal__footer">
          <span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>
          <span><kbd>↵</kbd> open</span>
          <span><kbd>esc</kbd> close</span>
        </div>
      </div>
    </div>
  )
}
