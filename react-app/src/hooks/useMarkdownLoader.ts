import { useState, useEffect } from 'react'
import { parseFrontMatter, type ParsedMarkdown } from '../utils/frontmatter'

// Eagerly load all markdown files at compile time as raw strings.
// Individual .md files are small (1-10KB each), and total content is ~3-5MB,
// which Vite handles well in a single bundle. This lets us:
// 1. Build the path map from front matter permalinks
// 2. Serve content instantly without async loading
const markdownModules = import.meta.glob<string>(
  [
    '../../../problem_soulutions/**/*.md',
    '../../../system_design/**/*.md',
    '../../../low_level_design/**/*.md',
    '../../../quick_reference/**/*.md',
    '../../../pattern/**/*.md',
    '../../../bytebytego_content/*/*.md',
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
  // Strip the Vite base path prefix (e.g. /cses-analyses on GitHub Pages, / on Vercel)
  const basePrefix = import.meta.env.BASE_URL.replace(/\/$/, '')
  if (basePrefix) {
    permalink = permalink.replace(new RegExp(`^${basePrefix}`), '')
  }
  return permalink || null
}

// Convert a ByteByteGo file path to a URL
// e.g. "bytebytego_content/system-design-interview/005_design-a-rate-limiter" → "/bytebytego/system-design-interview/design-a-rate-limiter"
// e.g. "bytebytego_content/coding-patterns/01-01_two-pointers_pair-sum-sorted" → "/bytebytego/coding-patterns/two-pointers/pair-sum-sorted"
function bytebytegUrlFromPath(filePath: string): string | null {
  const match = filePath.match(/bytebytego_content\/([^/]+)\/(.+)$/)
  if (!match) return null
  const courseKey = match[1]
  const filename = match[2] // e.g. "005_design-a-rate-limiter" or "01-01_two-pointers_pair-sum-sorted"

  // Sectioned course (coding-patterns): chapter is "NN-NN", slug has section/lesson
  const sectionedMatch = filename.match(/^\d+-\d+_(.+)_(.+)$/)
  if (sectionedMatch) {
    return `/bytebytego/${courseKey}/${sectionedMatch[1]}/${sectionedMatch[2]}`
  }

  // Flat course: chapter is "NNN", slug is the rest
  const flatMatch = filename.match(/^\d+_(.+)$/)
  if (flatMatch) {
    return `/bytebytego/${courseKey}/${flatMatch[1]}`
  }

  return `/bytebytego/${courseKey}/${filename}`
}

// Clean ByteByteGo export artifacts:
// 1. Rewrite image URLs from bytebytego.com to local paths
// 2. Remove duplicate images (export includes light+dark mode duplicates, sometimes non-adjacent)
// 3. Fix triple-rendered math: "O(n2)O(n^2)O(n2)" → "O(n²)" (keep first/plain version)
//    and standalone letter triples like "nnn" → "n"
export function cleanByteBytGoContent(raw: string): string {
  const baseUrl = import.meta.env.BASE_URL
  raw = raw.replaceAll('https://bytebytego.com/images/', baseUrl + 'images/')

  // Remove duplicate images (export includes light+dark mode duplicates).
  // Pass 1: consecutive duplicates separated only by blank lines.
  raw = raw.replace(/(!\[[\s\S]*?\]\(([^)]+)\))\s*\n\s*!\[[\s\S]*?\]\(\2\)/g, '$1')
  // Pass 2: non-consecutive duplicates — keep first occurrence of each image URL.
  const seenImageUrls = new Set<string>()
  raw = raw.replace(/!\[[\s\S]*?\]\(([^)]+)\)/g, (match, url) => {
    if (seenImageUrls.has(url)) return ''
    seenImageUrls.add(url)
    return match
  })

  // Fix triple math: X(expr1)X(expr2)X(expr1) → X(expr1)
  // The export repeats each expression 3 times: plain, LaTeX, plain
  // We keep the first (plain/Unicode) version which renders well without KaTeX
  raw = raw.replace(/([A-Za-z])\(([^)]+)\)\1\([^)]+\)\1\(\2\)/g, '$1($2)')

  // Fix standalone letter triples: "nnn" → "n", "mmm" → "m"
  raw = raw.replace(/(?<![a-zA-Z])([a-z])\1\1(?![a-zA-Z])/g, '$1')

  return raw
}

// Build a lookup map from URL path → glob key
// Registers both the file-path-based URL and the front matter permalink (if different).
function buildPathMap(): Map<string, string> {
  const pathMap = new Map<string, string>()

  for (const key of Object.keys(markdownModules)) {
    // Keys look like:
    //   "../../../problem_soulutions/introductory_problems/summary.md" (from parent dir)
    //   "../../content_index.md" or "../../content_about.md" (local files)
    //   "../../../bytebytego_content/system-design-interview/005_design-a-rate-limiter.md"
    let urlPath = key.replace(/^(\.\.\/)+/, '').replace(/\.md$/, '')

    // ByteByteGo content: use special path mapping
    if (urlPath.startsWith('bytebytego_content/')) {
      const bbgUrl = bytebytegUrlFromPath(urlPath)
      if (bbgUrl) {
        pathMap.set(bbgUrl, key)
      }
      continue
    }

    // Strip the "content_" prefix for local files
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

    // Clean up ByteByteGo content: rewrite image URLs, remove duplicate images,
    // and fix triple-rendered math expressions from the export format
    let raw = markdownModules[globKey]
    if (globKey.includes('bytebytego_content/')) {
      raw = cleanByteBytGoContent(raw)
    }

    setData(parseFrontMatter(raw))
    setLoading(false)
  }, [routePath])

  return { loading, error, data }
}
