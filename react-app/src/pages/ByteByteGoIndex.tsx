import { Link } from 'react-router-dom'
import coursesData from '../../../bytebytego_courses.json'

interface Course {
  key: string
  title: string
  authors: string
  lessons: number
  students: number
  chapters: { chapter: number | string; title: string; slug: string }[]
}

const courses = (coursesData as Course[]).filter(c => c.chapters.length > 0)

export default function ByteByteGoIndex() {
  return (
    <div className="bytebytego-index">
      <section className="hero">
        <h1 className="hero__title">ByteByteGo Courses</h1>
        <p className="hero__subtitle">
          System design, coding patterns, ML/GenAI design, and more from ByteByteGo.
        </p>
        <div className="hero__stats">
          <div className="hero__stat">
            <span className="hero__stat-number">{courses.length}</span>
            <span className="hero__stat-label">Courses</span>
          </div>
          <div className="hero__stat">
            <span className="hero__stat-number">
              {courses.reduce((sum, c) => sum + c.chapters.length, 0)}
            </span>
            <span className="hero__stat-label">Lessons</span>
          </div>
        </div>
      </section>

      <section className="categories">
        <h2 className="section-title">All Courses</h2>
        <div className="categories__grid">
          {courses.map((course) => (
            <Link
              key={course.key}
              to={`/bytebytego/${course.key}`}
              className="category-card"
              style={{ '--accent': '#f97316' } as React.CSSProperties}
            >
              <div className="category-card__icon">
                <img
                  src={`${import.meta.env.BASE_URL}covers/${course.key}.png`}
                  alt={course.title}
                  className="course-cover-thumb"
                />
              </div>
              <div className="category-card__body">
                <h3 className="category-card__title">{course.title}</h3>
                <p className="category-card__desc">{course.authors}</p>
              </div>
              <span className="category-card__count">{course.chapters.length}</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
