import { useState, useEffect, useCallback, useMemo, useRef } from 'react'

interface TocItem {
  level: number
  text: string
  id: string
}

interface TableOfContentsProps {
  content: string
}

// Match rehype-slug's ID generation (github-slugger style)
function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/<[^>]*>/g, '')           // strip HTML tags
    .replace(/[^\w\s-]/g, '')          // remove non-word chars (except spaces and hyphens)
    .replace(/\s+/g, '-')             // spaces to hyphens
    .replace(/-+/g, '-')              // collapse multiple hyphens
    .replace(/^-|-$/g, '')            // trim leading/trailing hyphens
}

function extractHeadings(markdown: string): TocItem[] {
  const headings: TocItem[] = []
  const slugCounts = new Map<string, number>()
  // Strip code blocks first so we don't pick up headings inside them
  const stripped = markdown.replace(/```[\s\S]*?```/g, '')
  const regex = /^(#{2,3})\s+(.+)$/gm
  let match
  while ((match = regex.exec(stripped)) !== null) {
    const level = match[1].length
    // Strip inline markdown formatting from heading text
    const text = match[2]
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\*(.+?)\*/g, '$1')
      .replace(/`(.+?)`/g, '$1')
      .replace(/\[(.+?)\]\(.*?\)/g, '$1')
      .trim()
    let id = slugify(text)
    // Handle duplicate slugs (same as github-slugger / rehype-slug)
    const count = slugCounts.get(id) || 0
    slugCounts.set(id, count + 1)
    if (count > 0) id = `${id}-${count}`
    headings.push({ level, text, id })
  }
  return headings
}

export default function TableOfContents({ content }: TableOfContentsProps) {
  const headings = useMemo(() => extractHeadings(content), [content])
  const [activeId, setActiveId] = useState('')
  const observerRef = useRef<IntersectionObserver | null>(null)

  // Set up IntersectionObserver to track which heading is in view
  useEffect(() => {
    if (headings.length === 0) return

    // Small delay to ensure headings are rendered with IDs
    const timer = setTimeout(() => {
      const elements = headings
        .map(h => document.getElementById(h.id))
        .filter(Boolean) as HTMLElement[]

      if (elements.length === 0) return

      observerRef.current = new IntersectionObserver(
        (entries) => {
          // Find the topmost visible heading
          const visible = entries.filter(e => e.isIntersecting)
          if (visible.length > 0) {
            // Pick the one closest to the top
            const top = visible.reduce((a, b) =>
              a.boundingClientRect.top < b.boundingClientRect.top ? a : b
            )
            setActiveId(top.target.id)
          }
        },
        {
          rootMargin: '0px 0px -70% 0px',
          threshold: 0,
        }
      )

      elements.forEach(el => observerRef.current!.observe(el))
    }, 100)

    return () => {
      clearTimeout(timer)
      observerRef.current?.disconnect()
    }
  }, [headings])

  const handleClick = useCallback((e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault()
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
      // Update URL hash without scrolling
      window.history.replaceState(null, '', `#${id}`)
      setActiveId(id)
    }
  }, [])

  // Don't render TOC for pages with fewer than 2 headings
  if (headings.length < 2) return null

  return (
    <nav className="toc" aria-label="Table of contents">
      <h4 className="toc__title">On this page</h4>
      <ul className="toc__list">
        {headings.map((h) => (
          <li
            key={h.id}
            className={`toc__item toc__item--h${h.level}${activeId === h.id ? ' toc__item--active' : ''}`}
          >
            <a
              href={`#${h.id}`}
              onClick={(e) => handleClick(e, h.id)}
            >
              {h.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  )
}
