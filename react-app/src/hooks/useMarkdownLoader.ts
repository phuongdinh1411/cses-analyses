import { useState, useEffect } from 'react'
import { parseFrontMatter, type ParsedMarkdown } from '../utils/frontmatter'

// Eagerly load all markdown files at compile time as raw strings.
// Individual .md files are small (1-10KB each), and total content is ~3-5MB,
// which Vite handles well in a single bundle. This lets us:
// 1. Build the path map from front matter permalinks
// 2. Serve content instantly without async loading
const markdownModules = import.meta.glob<string>(
  [
    '../../content_problem_soulutions/**/*.md',
    '../../content_system_design/**/*.md',
    '../../content_low_level_design/**/*.md',
    '../../content_quick_reference/**/*.md',
    '../../content_pattern/**/*.md',
    '../../content_index.md',
    '../../content_about.md',
  ],
  { query: '?raw', import: 'default', eager: true }
)

// Extract permalink from raw markdown front matter (quick regex, no full parse)
function extractPermalink(raw: string): string | null {
  const match = raw.match(/^---\r?\n[\s\S]*?\r?\n---/)
  if (!match) return null
  const pmatch = match[0].match(/^permalink:\s*(.+)$/m)
  if (!pmatch) return null
  let permalink = pmatch[1].trim().replace(/^['"]|['"]$/g, '')
  // Strip Jekyll baseurl prefix
  permalink = permalink.replace(/^\/cses-analyses/, '')
  return permalink || null
}

// Build a lookup map from URL path → glob key
// Registers both the file-path-based URL and the front matter permalink (if different).
function buildPathMap(): Map<string, string> {
  const pathMap = new Map<string, string>()

  for (const key of Object.keys(markdownModules)) {
    // key looks like "../../content_problem_soulutions/introductory_problems/summary.md"
    let urlPath = key.replace(/^\.\.\/\.\.\//, '').replace(/\.md$/, '')

    // Strip the "content_" prefix
    urlPath = urlPath.replace(/^content_/, '')

    // Handle index files
    if (urlPath.endsWith('/index')) {
      urlPath = urlPath.slice(0, -5) // remove "index", keep trailing "/"
    }

    // The root index.md maps to "/"
    if (urlPath === 'index') {
      pathMap.set('/', key)
    } else {
      pathMap.set('/' + urlPath, key)
    }

    // Also register the front matter permalink as an alias
    const permalink = extractPermalink(markdownModules[key])
    if (permalink) {
      const withoutSlash = permalink.replace(/\/$/, '') || '/'
      const withSlash = permalink.endsWith('/') ? permalink : permalink + '/'
      if (!pathMap.has(permalink)) pathMap.set(permalink, key)
      if (!pathMap.has(withoutSlash)) pathMap.set(withoutSlash, key)
      if (!pathMap.has(withSlash)) pathMap.set(withSlash, key)
    }
  }

  return pathMap
}

const pathMap = buildPathMap()

export interface UseMarkdownResult {
  loading: boolean
  error: string | null
  data: ParsedMarkdown | null
}

export function useMarkdownLoader(routePath: string): UseMarkdownResult {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<ParsedMarkdown | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)

    // Normalize: decode, strip trailing slash (except root)
    const normalized = decodeURIComponent(routePath).replace(/\/$/, '') || '/'

    // Try exact match, then with trailing slash
    let globKey = pathMap.get(normalized) ?? pathMap.get(normalized + '/')

    // If still not found, try decoded comparison across all entries
    if (!globKey) {
      for (const [path, key] of pathMap.entries()) {
        const decodedPath = decodeURIComponent(path).replace(/\/$/, '') || '/'
        if (decodedPath === normalized) {
          globKey = key
          break
        }
      }
    }

    if (!globKey) {
      setError(`Page not found: ${routePath}`)
      setLoading(false)
      return
    }

    setData(parseFrontMatter(markdownModules[globKey]))
    setLoading(false)
  }, [routePath])

  return { loading, error, data }
}
