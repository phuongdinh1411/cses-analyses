import { useParams, Link } from 'react-router-dom'
import coursesData from '../../../bytebytego_courses.json'

interface Chapter {
  chapter: number | string
  title: string
  slug: string
}

interface Course {
  key: string
  title: string
  authors: string
  chapters: Chapter[]
}

const courseMap = new Map(
  (coursesData as Course[]).map(c => [c.key, c])
)

function chapterUrl(courseKey: string, slug: string): string {
  return `/bytebytego/${courseKey}/${slug}`
}

function isSectioned(course: Course): boolean {
  return course.chapters.some(ch => String(ch.chapter).includes('-'))
}

interface Section {
  title: string
  chapters: { title: string; url: string }[]
}

function buildSections(course: Course): Section[] {
  const sections: Section[] = []
  let currentSection: Section | null = null

  for (const ch of course.chapters) {
    const chStr = String(ch.chapter)
    const suffix = chStr.split('-')[1]

    if (suffix === '00') {
      // New section
      currentSection = {
        title: ch.title.replace(/^Introduction to /, ''),
        chapters: [],
      }
      sections.push(currentSection)
    }

    if (currentSection) {
      currentSection.chapters.push({
        title: ch.title,
        url: chapterUrl(course.key, ch.slug),
      })
    }
  }

  return sections
}

export default function ByteBytegoCourseIndex() {
  const { courseKey } = useParams<{ courseKey: string }>()
  const course = courseKey ? courseMap.get(courseKey) : undefined

  if (!course) {
    return (
      <div className="error-container">
        <h1>Course Not Found</h1>
        <p>No course found for "{courseKey}"</p>
        <Link to="/bytebytego">Back to all courses</Link>
      </div>
    )
  }

  const sectioned = isSectioned(course)

  return (
    <div className="course-index">
      <nav className="breadcrumbs" aria-label="Breadcrumb">
        <span className="breadcrumbs__item">
          <Link to="/bytebytego" className="breadcrumbs__link">ByteByteGo</Link>
        </span>
        <span className="breadcrumbs__item">
          <span className="breadcrumbs__sep">/</span>
          <span className="breadcrumbs__current">{course.title}</span>
        </span>
      </nav>

      <h1 className="page-title">{course.title}</h1>
      <p className="course-index__meta">
        {course.authors} &middot; {course.chapters.length} lessons
      </p>

      {sectioned ? (
        <div className="course-sections">
          {buildSections(course).map((section, i) => (
            <div key={i} className="course-section">
              <h2 className="course-section__title">{section.title}</h2>
              <ol className="course-section__list">
                {section.chapters.map((ch) => (
                  <li key={ch.url}>
                    <Link to={ch.url}>{ch.title}</Link>
                  </li>
                ))}
              </ol>
            </div>
          ))}
        </div>
      ) : (
        <ol className="course-chapter-list">
          {course.chapters.map((ch) => (
            <li key={ch.slug}>
              <Link to={chapterUrl(course.key, ch.slug)}>{ch.title}</Link>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}
