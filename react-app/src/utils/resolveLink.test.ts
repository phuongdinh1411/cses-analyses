// Run: node src/utils/resolveLink.test.ts
import { resolveLink, sourceDirOf, type ResolvedLink } from './resolveLink.ts'

const PAGES = '/cses-analyses/'
const VERCEL = '/'

const cases: [href: string, sourceDir: string, base: string, expected: ResolvedLink][] = [
  // Root-relative routes are left base-free; the router's basename adds the base.
  ['/pattern/Heap#x', '/system_design/', PAGES, { type: 'route', to: '/pattern/Heap#x' }],
  ['/pattern/Heap#x', '/system_design/', VERCEL, { type: 'route', to: '/pattern/Heap#x' }],
  ['/quick_reference/', '/worldquant/', PAGES, { type: 'route', to: '/quick_reference/' }],
  // Already base-prefixed: not doubled, and still valid on Vercel.
  ['/cses-analyses/system_design/design-youtube', '/system_design/', PAGES, { type: 'route', to: '/system_design/design-youtube' }],
  ['/cses-analyses/system_design/design-youtube', '/system_design/', VERCEL, { type: 'route', to: '/system_design/design-youtube' }],
  ['/cses-analyses', '/', PAGES, { type: 'route', to: '/' }],
  ['/cses-analysesX/a', '/', PAGES, { type: 'route', to: '/cses-analysesX/a' }],
  // Relative .md links resolve against the source file's directory.
  ['bitly.md', '/system_design/hellointerview/', PAGES, { type: 'route', to: '/system_design/hellointerview/bitly' }],
  ['concepts/primer.md', '/system_design/sds/', PAGES, { type: 'route', to: '/system_design/sds/concepts/primer' }],
  ['../sds/rate-limiter.md#a', '/system_design/hellointerview/', VERCEL, { type: 'route', to: '/system_design/sds/rate-limiter#a' }],
  ['./consistent-hashing.md', '/system_design/', PAGES, { type: 'route', to: '/system_design/consistent-hashing' }],
  ['hellointerview/index.md', '/system_design/', PAGES, { type: 'route', to: '/system_design/hellointerview/' }],
  ['../index.md', '/system_design/sds/', PAGES, { type: 'route', to: '/system_design/' }],
  ['../../../x.md', '/a/', PAGES, { type: 'route', to: '/x' }],
  // Absolute .md links.
  ['/system_design/design-payment-system.md#idempotency', '/', PAGES, { type: 'route', to: '/system_design/design-payment-system#idempotency' }],
  ['/cses-analyses/pattern/Heap.md', '/', PAGES, { type: 'route', to: '/pattern/Heap' }],
  // Relative links without .md and directory links.
  ['bridges_analysis', '/problem_soulutions/graph_algorithms/', PAGES, { type: 'route', to: '/problem_soulutions/graph_algorithms/bridges_analysis' }],
  ['Session%2001%20-%20Dynamic%20Array/', '/problem_soulutions/Blue/', PAGES, { type: 'route', to: '/problem_soulutions/Blue/Session%2001%20-%20Dynamic%20Array/' }],
  ['../', '/system_design/sds/', PAGES, { type: 'route', to: '/system_design/' }],
  ['page.md?v=1#h', '/a/', PAGES, { type: 'route', to: '/a/page?v=1#h' }],
  // Untouched.
  ['https://example.com/a.md', '/', PAGES, { type: 'external', href: 'https://example.com/a.md' }],
  ['http://example.com', '/', PAGES, { type: 'external', href: 'http://example.com' }],
  ['mailto:a@b.c', '/', PAGES, { type: 'external', href: 'mailto:a@b.c' }],
  ['//cdn.example.com/x', '/', PAGES, { type: 'external', href: '//cdn.example.com/x' }],
  ['#summary', '/system_design/', PAGES, { type: 'anchor', href: '#summary' }],
]

const dirCases: [filePath: string, expected: string][] = [
  ['system_design/sds/index.md', '/system_design/sds/'],
  ['system_design/design-youtube.md', '/system_design/'],
  ['index.md', '/'],
]

let failures = 0
for (const [href, dir, base, expected] of cases) {
  const actual = resolveLink(href, dir, base)
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    failures++
    console.error(`FAIL resolveLink(${href}, ${dir}, ${base}) = ${JSON.stringify(actual)}, expected ${JSON.stringify(expected)}`)
  }
}
for (const [filePath, expected] of dirCases) {
  const actual = sourceDirOf(filePath)
  if (actual !== expected) {
    failures++
    console.error(`FAIL sourceDirOf(${filePath}) = ${actual}, expected ${expected}`)
  }
}

const total = cases.length + dirCases.length
if (failures > 0) throw new Error(`${failures}/${total} link resolution checks failed`)
console.log(`${total} link resolution checks passed`)
