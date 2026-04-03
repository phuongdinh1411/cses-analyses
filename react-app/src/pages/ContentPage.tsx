import { useEffect, useMemo } from 'react'
import { useLocation, Link } from 'react-router-dom'
import { useMarkdownLoader } from '../hooks/useMarkdownLoader'
import MarkdownRenderer from '../components/MarkdownRenderer'
import { getPageNavContext } from '../utils/pageNav'

export default function ContentPage() {
  const location = useLocation()
  const { loading, error, data } = useMarkdownLoader(location.pathname)

  const navContext = useMemo(
    () => getPageNavContext(location.pathname),
    [location.pathname]
  )

  // Scroll to top on navigation, or to hash if present
  useEffect(() => {
    if (location.hash) {
      const el = document.getElementById(location.hash.slice(1))
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' })
        return
      }
    }
    window.scrollTo(0, 0)
  }, [location.pathname, location.hash])

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner" />
        <p>Loading...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <h1>404</h1>
        <p>{error}</p>
        <p>Check the URL or use the sidebar to navigate.</p>
      </div>
    )
  }

  if (!data) return null

  const title = data.frontMatter.title
  // Skip rendering the page title if the markdown content already starts with an h1
  const contentStartsWithH1 = /^\s*#\s+/.test(data.content)

  return (
    <>
      {title && <title>{title} | CSES Analyses</title>}

      {/* Breadcrumbs */}
      {navContext.breadcrumbs.length > 1 && (
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          {navContext.breadcrumbs.map((crumb, i) => (
            <span key={crumb.url} className="breadcrumbs__item">
              {i > 0 && <span className="breadcrumbs__sep">/</span>}
              {i < navContext.breadcrumbs.length - 1 ? (
                <Link to={crumb.url} className="breadcrumbs__link">
                  {crumb.title}
                </Link>
              ) : (
                <span className="breadcrumbs__current">{crumb.title}</span>
              )}
            </span>
          ))}
        </nav>
      )}

      {/* Page Title — only if markdown doesn't already start with an h1 */}
      {title && !contentStartsWithH1 && <h1 className="page-title">{title}</h1>}

      {/* Content */}
      <MarkdownRenderer content={data.content} />

      {/* Prev/Next Navigation */}
      {(navContext.prev || navContext.next) && (
        <nav className="page-nav" aria-label="Page navigation">
          <div className="page-nav__prev">
            {navContext.prev && (
              <Link to={navContext.prev.url} className="page-nav__link">
                <span className="page-nav__label">Previous</span>
                <span className="page-nav__title">{navContext.prev.title}</span>
              </Link>
            )}
          </div>
          <div className="page-nav__next">
            {navContext.next && (
              <Link to={navContext.next.url} className="page-nav__link page-nav__link--next">
                <span className="page-nav__label">Next</span>
                <span className="page-nav__title">{navContext.next.title}</span>
              </Link>
            )}
          </div>
        </nav>
      )}
    </>
  )
}
