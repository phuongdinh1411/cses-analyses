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

// Get the first leaf URL from a nav item (for parent nodes without content)
function firstLeafUrl(item: NavItem): string {
  if (item.children && item.children.length > 0) {
    return firstLeafUrl(item.children[0])
  }
  return item.url
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

// Resolve breadcrumb URLs: parent nodes without content get their first leaf URL
function resolveBreadcrumbUrls(
  breadcrumbs: BreadcrumbItem[],
  navItems: NavItem[]
): BreadcrumbItem[] {
  return breadcrumbs.map(crumb => {
    const navItem = findNavItem(navItems, crumb.url)
    if (navItem && navItem.children && navItem.children.length > 0) {
      return { ...crumb, url: firstLeafUrl(navItem) }
    }
    return crumb
  })
}

// Find a NavItem by its URL in the tree
function findNavItem(items: NavItem[], url: string): NavItem | null {
  for (const item of items) {
    if (item.url === url) return item
    if (item.children) {
      const found = findNavItem(item.children, url)
      if (found) return found
    }
  }
  return null
}

export function getPageNavContext(pathname: string): PageNavContext {
  const normalized = decodeURIComponent(pathname).replace(/\/$/, '') || '/'

  // Breadcrumbs — find trail then resolve parent URLs to first leaf
  const rawBreadcrumbs = findBreadcrumbs(navigationData, normalized, []) ?? []
  const breadcrumbs = resolveBreadcrumbUrls(rawBreadcrumbs, navigationData)

  // Prev/Next from flattened leaf list
  const leaves = flattenLeaves(navigationData)
  const currentIndex = leaves.findIndex(
    (item) => (decodeURIComponent(item.url).replace(/\/$/, '') || '/') === normalized
  )

  const prev = currentIndex > 0 ? leaves[currentIndex - 1] : null
  const next = currentIndex >= 0 && currentIndex < leaves.length - 1 ? leaves[currentIndex + 1] : null

  return { breadcrumbs, prev, next }
}
