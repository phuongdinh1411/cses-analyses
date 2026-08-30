import { useState, useCallback, useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import MobileNavToggle from './MobileNavToggle'
import SearchModal from './SearchModal'

export default function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [sidebarHidden, setSidebarHidden] = useState(
    () => localStorage.getItem('sidebarHidden') === 'true'
  )

  const toggleMobile = useCallback(() => {
    setMobileOpen(prev => !prev)
  }, [])

  const closeMobile = useCallback(() => {
    setMobileOpen(false)
  }, [])

  const toggleSidebar = useCallback(() => {
    setSidebarHidden(prev => !prev)
  }, [])

  // Persist sidebar collapse choice across pages/reloads
  useEffect(() => {
    localStorage.setItem('sidebarHidden', String(sidebarHidden))
  }, [sidebarHidden])

  // Cmd+K / Ctrl+K to open search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setSearchOpen(prev => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <>
      <MobileNavToggle active={mobileOpen} onToggle={toggleMobile} />
      {sidebarHidden && (
        <button
          className="sidebar-show-btn"
          onClick={toggleSidebar}
          aria-label="Show sidebar"
          title="Show sidebar"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
      )}
      <div className="container">
        <Sidebar
          mobileOpen={mobileOpen}
          hidden={sidebarHidden}
          onLinkClick={closeMobile}
          onSearchClick={() => setSearchOpen(true)}
          onToggleHidden={toggleSidebar}
        />
        <main className="main-content">
          <div className="content">
            <Outlet />
          </div>
        </main>
      </div>
      <SearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
    </>
  )
}
