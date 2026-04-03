import coursesData from '../../../bytebytego_courses.json'
import type { NavItem } from './navigation'

interface Chapter {
  chapter: number | string
  title: string
  slug: string
  free: boolean
}

interface Course {
  key: string
  title: string
  chapters: Chapter[]
}

const courses = coursesData as Course[]

// Build URL for a chapter based on course type
function chapterUrl(courseKey: string, slug: string): string {
  return `/bytebytego/${courseKey}/${slug}`
}

// Build nav items for a sectioned course (coding-patterns)
// Chapters like "01-00", "01-01" are grouped by prefix
function buildSectionedNav(course: Course): NavItem[] {
  const sections = new Map<string, { title: string; children: NavItem[] }>()

  for (const ch of course.chapters) {
    const chStr = String(ch.chapter)
    const prefix = chStr.split('-')[0] // e.g. "01"
    const suffix = chStr.split('-')[1] // e.g. "00", "01"

    if (!sections.has(prefix)) {
      sections.set(prefix, { title: '', children: [] })
    }

    const section = sections.get(prefix)!

    if (suffix === '00') {
      // Introduction chapter — use its title as the section title
      // Strip "Introduction to " prefix for cleaner section names
      section.title = ch.title.replace(/^Introduction to /, '')
      // Still add it as a nav item
      section.children.push({
        title: ch.title,
        url: chapterUrl(course.key, ch.slug),
      })
    } else {
      section.children.push({
        title: ch.title,
        url: chapterUrl(course.key, ch.slug),
      })
    }
  }

  return Array.from(sections.values()).map(s => ({
    title: s.title || 'Section',
    url: s.children[0]?.url || '',
    children: s.children,
  }))
}

// Build nav items for a flat course (numbered chapters)
function buildFlatNav(course: Course): NavItem[] {
  return course.chapters.map(ch => ({
    title: ch.title,
    url: chapterUrl(course.key, ch.slug),
  }))
}

function isSectioned(course: Course): boolean {
  return course.chapters.some(ch => String(ch.chapter).includes('-'))
}

// Build the full ByteByteGo navigation tree
export function buildByteByteGoNavigation(): NavItem[] {
  const courseItems: NavItem[] = courses
    .filter(c => c.chapters.length > 0)
    .map(course => ({
      title: course.title,
      url: `/bytebytego/${course.key}`,
      children: isSectioned(course)
        ? buildSectionedNav(course)
        : buildFlatNav(course),
    }))

  return [
    {
      title: 'ByteByteGo',
      url: '/bytebytego',
      children: courseItems,
    },
  ]
}

export const bytebytegNavigationData = buildByteByteGoNavigation()
