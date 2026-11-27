export type ResolvedLink =
  | { type: 'external'; href: string }
  | { type: 'anchor'; href: string }
  | { type: 'route'; to: string }

const SCHEME_RE = /^[a-z][a-z\d+.-]*:/i

// Content written for GitHub Pages hard-codes this prefix; strip it on every deployment.
const PAGES_BASE = '/cses-analyses/'

function withTrailingSlash(path: string): string {
  return path.endsWith('/') ? path : path + '/'
}

function stripBase(path: string, base: string): string {
  for (const prefix of [withTrailingSlash(base), PAGES_BASE]) {
    if (prefix !== '/' && withTrailingSlash(path).startsWith(prefix)) {
      return path.slice(prefix.length - 1) || '/'
    }
  }
  return path
}

function joinPath(dir: string, relative: string): string {
  const segments = dir.split('/').filter(Boolean)
  const parts = relative.split('/')
  for (const part of parts) {
    if (part === '' || part === '.') continue
    if (part === '..') segments.pop()
    else segments.push(part)
  }
  const last = parts[parts.length - 1]
  const isDir = last === '' || last === '.' || last === '..'
  const joined = '/' + segments.join('/')
  return isDir && segments.length > 0 ? joined + '/' : joined
}

/**
 * Map a markdown href to an SPA route (without the deploy base; the router adds it).
 * `sourceDir` is the directory of the markdown file, e.g. "/system_design/sds/".
 */
export function resolveLink(href: string, sourceDir: string, base = '/'): ResolvedLink {
  if (SCHEME_RE.test(href) || href.startsWith('//')) return { type: 'external', href }

  const suffixAt = href.search(/[?#]/)
  const rawPath = suffixAt === -1 ? href : href.slice(0, suffixAt)
  const suffix = suffixAt === -1 ? '' : href.slice(suffixAt)
  if (rawPath === '') return { type: 'anchor', href }

  const path = rawPath.startsWith('/')
    ? stripBase(rawPath, base)
    : joinPath(withTrailingSlash(sourceDir), rawPath)

  const route = path.replace(/\.md$/i, '').replace(/(^|\/)index$/, '$1') || '/'
  return { type: 'route', to: route + suffix }
}

/** Directory of a markdown source path relative to the repo root, as a route prefix. */
export function sourceDirOf(filePath: string): string {
  const slash = filePath.lastIndexOf('/')
  return slash === -1 ? '/' : '/' + filePath.slice(0, slash + 1)
}
