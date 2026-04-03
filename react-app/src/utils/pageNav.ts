import { navigationData, type NavItem } from '../data/navigation'

export interface BreadcrumbItem {
  title: string
  url: string
}

export interface PageNavContext {
  breadcrumbs: BreadcrumbItem[]
  prev: NavItem | null
  next: NavItem | null
}

// Flatten the entire nav tree into an ordered list of leaf links
function flattenLeaves(items: NavItem[]): NavItem[] {
  const result: NavItem[] = []
  for (const item of items) {
    if (item.children && item.children.length > 0) {
      result.push(...flattenLeaves(item.children))
    } else {
      result.push(item)
    }
  }
  return result
}

// Find breadcrumb trail to a path in the nav tree
function findBreadcrumbs(
  items: NavItem[],
  targetPath: string,
  trail: BreadcrumbItem[]
): BreadcrumbItem[] | null {
  for (const item of items) {
    const itemPath = decodeURIComponent(item.url).replace(/\/$/, '') || '/'
    const currentTrail = [...trail, { title: item.title, url: item.url }]

    if (itemPath === targetPath) {
      return currentTrail
    }

    if (item.children) {
      const found = findBreadcrumbs(item.children, targetPath, currentTrail)
      if (found) return found
    }
  }
  return null
}

export function getPageNavContext(pathname: string): PageNavContext {
  const normalized = decodeURIComponent(pathname).replace(/\/$/, '') || '/'

  // Breadcrumbs
  const breadcrumbs = findBreadcrumbs(navigationData, normalized, []) ?? []

  // Prev/Next from flattened leaf list
  const leaves = flattenLeaves(navigationData)
  const currentIndex = leaves.findIndex(
    (item) => (decodeURIComponent(item.url).replace(/\/$/, '') || '/') === normalized
  )

  const prev = currentIndex > 0 ? leaves[currentIndex - 1] : null
  const next = currentIndex >= 0 && currentIndex < leaves.length - 1 ? leaves[currentIndex + 1] : null

  return { breadcrumbs, prev, next }
}
