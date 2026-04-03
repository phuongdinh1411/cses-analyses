// Build a search index from all eagerly-loaded markdown files.
// Reuses the same glob as useMarkdownLoader — since both are eager imports,
// Vite deduplicates them into a single bundle chunk.

const markdownModules = import.meta.glob<string>(
  [
    '../../../problem_soulutions/**/*.md',
    '../../../system_design/**/*.md',
    '../../../low_level_design/**/*.md',
    '../../../quick_reference/**/*.md',
    '../../../pattern/**/*.md',
    '../../content_index.md',
    '../../content_about.md',
  ],
  { query: '?raw', import: 'default', eager: true }
)

export interface SearchResult {
  title: string
  url: string
  snippet: string
  score: number
}

interface SearchEntry {
  title: string
  url: string
  content: string // plain text, front matter stripped
}

function extractTitle(raw: string): string {
  // Try front matter title
  const fmMatch = raw.match(/^---\r?\n[\s\S]*?\r?\n---/)
  if (fmMatch) {
    const titleMatch = fmMatch[0].match(/^title:\s*["']?(.+?)["']?\s*$/m)
    if (titleMatch) return titleMatch[1]
  }
  // Fallback: first h1
  const h1Match = raw.match(/^#\s+(.+)$/m)
  if (h1Match) return h1Match[1]
  return 'Untitled'
}

function extractUrl(key: string, raw: string): string {
  // Try permalink
  const fmMatch = raw.match(/^---\r?\n[\s\S]*?\r?\n---/)
  if (fmMatch) {
    const pmatch = fmMatch[0].match(/^permalink:\s*(.+)$/m)
    if (pmatch) {
      let permalink = pmatch[1].trim().replace(/^['"]|['"]$/g, '')
      permalink = permalink.replace(/^\/cses-analyses/, '')
      if (permalink) return permalink.replace(/\/$/, '') || '/'
    }
  }
  // Derive from file path
  let urlPath = key.replace(/^(\.\.\/)+/, '').replace(/\.md$/, '')
  urlPath = urlPath.replace(/^content_/, '')
  if (urlPath.endsWith('/index')) urlPath = urlPath.slice(0, -5)
  if (urlPath === 'index') return '/'
  return '/' + urlPath
}

function stripMarkdown(raw: string): string {
  // Remove front matter
  let text = raw.replace(/^---\r?\n[\s\S]*?\r?\n---/, '')
  // Remove code blocks
  text = text.replace(/```[\s\S]*?```/g, '')
  // Remove inline code
  text = text.replace(/`[^`]+`/g, '')
  // Remove HTML tags
  text = text.replace(/<[^>]+>/g, '')
  // Remove markdown formatting
  text = text.replace(/[#*_~\[\]|>]/g, ' ')
  // Collapse whitespace
  text = text.replace(/\s+/g, ' ').trim()
  return text
}

// Build index once at module load
const searchIndex: SearchEntry[] = Object.entries(markdownModules).map(([key, raw]) => ({
  title: extractTitle(raw),
  url: extractUrl(key, raw),
  content: stripMarkdown(raw),
}))

export function search(query: string, maxResults = 15): SearchResult[] {
  if (!query || query.length < 2) return []

  const terms = query.toLowerCase().split(/\s+/).filter(Boolean)
  const results: SearchResult[] = []

  for (const entry of searchIndex) {
    const titleLower = entry.title.toLowerCase()
    const contentLower = entry.content.toLowerCase()

    let score = 0

    for (const term of terms) {
      // Title match (high weight)
      if (titleLower.includes(term)) {
        score += 10
        // Exact title match bonus
        if (titleLower === term || titleLower.startsWith(term + ' ')) score += 5
      }
      // Content match
      if (contentLower.includes(term)) {
        score += 1
        // Count occurrences (cap at 5 for scoring)
        const occurrences = Math.min((contentLower.split(term).length - 1), 5)
        score += occurrences * 0.5
      }
    }

    if (score > 0) {
      // Extract a snippet around the first match
      const snippet = extractSnippet(entry.content, terms)
      results.push({ title: entry.title, url: entry.url, snippet, score })
    }
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score)
  return results.slice(0, maxResults)
}

function extractSnippet(content: string, terms: string[]): string {
  const lower = content.toLowerCase()
  let bestPos = -1

  // Find the earliest occurrence of any term
  for (const term of terms) {
    const pos = lower.indexOf(term)
    if (pos !== -1 && (bestPos === -1 || pos < bestPos)) {
      bestPos = pos
    }
  }

  if (bestPos === -1) return content.slice(0, 120) + '...'

  // Extract context around the match
  const start = Math.max(0, bestPos - 40)
  const end = Math.min(content.length, bestPos + 100)
  let snippet = content.slice(start, end).trim()

  if (start > 0) snippet = '...' + snippet
  if (end < content.length) snippet = snippet + '...'

  return snippet
}
