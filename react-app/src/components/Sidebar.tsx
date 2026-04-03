import { useState, useEffect, useCallback, useMemo } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { navigationData, type NavItem } from '../data/navigation'

interface SidebarProps {
  mobileOpen: boolean
  onLinkClick: () => void
  onSearchClick?: () => void
}

// Check if an item or any of its descendants match the query
function itemMatchesQuery(item: NavItem, query: string): boolean {
  const q = query.toLowerCase()
  if (item.title.toLowerCase().includes(q)) return true
  if (item.children) {
    return item.children.some(child => itemMatchesQuery(child, q))
  }
  return false
}

// Filter nav tree, keeping parents that have matching descendants
function filterNavItems(items: NavItem[], query: string): NavItem[] {
  if (!query) return items
  return items
    .filter(item => itemMatchesQuery(item, query))
    .map(item => {
      if (!item.children) return item
      const filteredChildren = filterNavItems(item.children, query)
      return { ...item, children: filteredChildren.length > 0 ? filteredChildren : item.children }
    })
}

export default function Sidebar({ mobileOpen, onLinkClick, onSearchClick }: SidebarProps) {
  const location = useLocation()
  const currentPath = decodeURIComponent(location.pathname).replace(/\/$/, '') || '/'

  const [searchQuery, setSearchQuery] = useState('')

  // Track which nav sections are expanded
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set())

  // Auto-expand parents of the active link on route change
  useEffect(() => {
    const newExpanded = new Set<string>()

    function findAndExpand(items: NavItem[], parents: string[]): boolean {
      for (const item of items) {
        const itemUrl = decodeURIComponent(item.url).replace(/\/$/, '') || '/'
        if (itemUrl === currentPath) {
          parents.forEach(p => newExpanded.add(p))
          return true
        }
        if (item.children) {
          if (findAndExpand(item.children, [...parents, item.url])) {
            return true
          }
        }
      }
      return false
    }

    findAndExpand(navigationData, [])
    setExpandedItems(prev => {
      // Merge: keep previously expanded + auto-expand current path
      const merged = new Set(prev)
      newExpanded.forEach(url => merged.add(url))
      return merged
    })
  }, [currentPath])

  const toggleExpand = useCallback((url: string) => {
    setExpandedItems(prev => {
      const next = new Set(prev)
      if (next.has(url)) {
        next.delete(url)
      } else {
        next.add(url)
      }
      return next
    })
  }, [])

  // Close mobile sidebar on window resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768 && mobileOpen) {
        onLinkClick()
      }
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [mobileOpen, onLinkClick])

  // Filter nav items based on search query
  const filteredNav = useMemo(
    () => filterNavItems(navigationData, searchQuery),
    [searchQuery]
  )

  // When searching, expand all matching items so results are visible
  const isSearching = searchQuery.length > 0

  const isActive = (url: string) => {
    const normalized = decodeURIComponent(url).replace(/\/$/, '') || '/'
    return normalized === currentPath
  }

  const renderLevel4 = (items: NavItem[]) => (
    <ul className="nav__level4 expanded">
      {items.map(item => (
        <li key={item.url} className="nav__level4-item">
          <Link
            to={item.url}
            className={isActive(item.url) ? 'active' : ''}
            onClick={onLinkClick}
          >
            {item.title}
          </Link>
        </li>
      ))}
    </ul>
  )

  const renderLevel3 = (items: NavItem[]) => (
    <ul className={`nav__sub-sub-items expanded`}>
      {items.map(grandchild => {
        const hasChildren = grandchild.children && grandchild.children.length > 0
        const isExpanded = expandedItems.has(grandchild.url)

        return (
          <li key={grandchild.url} className="nav__sub-sub-item">
            {hasChildren ? (
              <a
                onClick={(e) => { e.preventDefault(); toggleExpand(grandchild.url) }}
                className={isActive(grandchild.url) ? 'active' : ''}
                role="button"
                tabIndex={0}
              >
                {grandchild.title}
              </a>
            ) : (
              <Link
                to={grandchild.url}
                className={isActive(grandchild.url) ? 'active' : ''}
                onClick={onLinkClick}
              >
                {grandchild.title}
              </Link>
            )}
            {hasChildren && (isExpanded || isSearching) && renderLevel4(grandchild.children!)}
          </li>
        )
      })}
    </ul>
  )

  const renderLevel2 = (items: NavItem[], parentUrl: string) => (
    <ul className={`nav__sub-items${(expandedItems.has(parentUrl) || isSearching) ? ' expanded' : ''}`}>
      {items.map(child => {
        const hasChildren = child.children && child.children.length > 0
        const isExpanded = expandedItems.has(child.url)

        return (
          <li key={child.url} className="nav__sub-item">
            {hasChildren ? (
              <a
                onClick={(e) => { e.preventDefault(); toggleExpand(child.url) }}
                className={isActive(child.url) ? 'active' : ''}
                role="button"
                tabIndex={0}
              >
                {child.title}
              </a>
            ) : (
              <Link
                to={child.url}
                className={isActive(child.url) ? 'active' : ''}
                onClick={onLinkClick}
              >
                {child.title}
              </Link>
            )}
            {hasChildren && (isExpanded || isSearching) && renderLevel3(child.children!)}
          </li>
        )
      })}
    </ul>
  )

  return (
    <nav className={`sidebar${mobileOpen ? ' mobile-open' : ''}`} id="sidebar">
      <h3>Learning</h3>
      {onSearchClick && (
        <button className="sidebar-search-btn" onClick={onSearchClick}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
          <span>Search...</span>
          <kbd>⌘K</kbd>
        </button>
      )}
      <div className="sidebar-search">
        <input
          type="text"
          className="sidebar-search__input"
          placeholder="Filter navigation..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {searchQuery && (
          <button
            className="sidebar-search__clear"
            onClick={() => setSearchQuery('')}
            aria-label="Clear search"
          >
            ×
          </button>
        )}
      </div>
      <ul className="nav__items">
        {filteredNav.map(item => {
          const hasChildren = item.children && item.children.length > 0

          return (
            <li key={item.url} className="nav__item">
              {hasChildren ? (
                <a
                  onClick={(e) => { e.preventDefault(); toggleExpand(item.url) }}
                  className={isActive(item.url) ? 'active' : ''}
                  role="button"
                  tabIndex={0}
                >
                  {item.title}
                </a>
              ) : (
                <Link
                  to={item.url}
                  className={isActive(item.url) ? 'active' : ''}
                  onClick={onLinkClick}
                >
                  {item.title}
                </Link>
              )}
              {hasChildren && renderLevel2(item.children!, item.url)}
            </li>
          )
        })}
      </ul>
    </nav>
  )
}
