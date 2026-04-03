import { Link } from 'react-router-dom'

const categories = [
  {
    icon: '📘',
    title: 'CSES Problem Set',
    description: 'Classic competitive programming: DP, graphs, trees, strings, geometry',
    count: '200+',
    url: '/problem_soulutions/introductory_problems/summary',
    color: '#3b82f6',
  },
  {
    icon: '🔵',
    title: 'Blue Curriculum',
    description: '19 sessions: arrays, sorting, BFS/DFS, shortest paths, MST',
    count: '19',
    url: '/problem_soulutions/Blue/summary',
    color: '#2563eb',
  },
  {
    icon: '🟠',
    title: 'Orange Curriculum',
    description: 'Advanced: backtracking, segment trees, number theory',
    count: '30+',
    url: '/problem_soulutions/Orange/summary',
    color: '#f59e0b',
  },
  {
    icon: '🏗️',
    title: 'System Design',
    description: 'Distributed systems, scalability patterns, architecture interviews',
    count: '17',
    url: '/system_design',
    color: '#8b5cf6',
  },
  {
    icon: '🧩',
    title: 'Low Level Design',
    description: 'OOP design problems for coding interviews',
    count: '33',
    url: '/low_level_design',
    color: '#ec4899',
  },
  {
    icon: '🔄',
    title: 'Patterns',
    description: 'Algorithm patterns: DP, graphs, trees, binary search, backtracking',
    count: '13',
    url: '/pattern/DP',
    color: '#10b981',
  },
]

const quickLinks = [
  {
    title: 'Study Guide',
    description: 'Learning path & interview prep',
    url: '/quick_reference/study_guide',
  },
  {
    title: 'Code Templates',
    description: 'Ready-to-use implementations',
    url: '/quick_reference/code_templates',
  },
  {
    title: 'Common Mistakes',
    description: 'Pitfalls to avoid',
    url: '/quick_reference/common_mistakes',
  },
]

const externalLinks = [
  { title: 'Awesome LeetCode Resources', url: 'https://github.com/ashishps1/awesome-leetcode-resources', desc: 'Curated patterns and guides' },
  { title: 'CSES Problem Set', url: 'https://cses.fi/problemset/', desc: 'Original problem source' },
  { title: 'Concurrency Interview', url: 'https://algomaster.io/learn/concurrency-interview/introduction-to-concurrency', desc: 'Introduction to concurrency' },
  { title: 'DSA Course Roadmap', url: 'https://algomaster.io/learn/dsa/course-roadmap', desc: 'Structured learning path' },
]

export default function HomePage() {
  return (
    <div className="homepage">
      {/* Hero */}
      <section className="hero">
        <h1 className="hero__title">DSA Problem Solutions</h1>
        <p className="hero__subtitle">
          A curated collection of algorithm problems with detailed solutions,
          system design guides, and interview preparation materials.
        </p>
        <div className="hero__stats">
          <div className="hero__stat">
            <span className="hero__stat-number">500+</span>
            <span className="hero__stat-label">Problems</span>
          </div>
          <div className="hero__stat">
            <span className="hero__stat-number">15</span>
            <span className="hero__stat-label">Categories</span>
          </div>
          <div className="hero__stat">
            <span className="hero__stat-number">17</span>
            <span className="hero__stat-label">System Designs</span>
          </div>
          <div className="hero__stat">
            <span className="hero__stat-number">13</span>
            <span className="hero__stat-label">Patterns</span>
          </div>
        </div>
      </section>

      {/* Category Cards */}
      <section className="categories">
        <h2 className="section-title">Problem Sets</h2>
        <div className="categories__grid">
          {categories.map((cat) => (
            <Link key={cat.url} to={cat.url} className="category-card" style={{ '--accent': cat.color } as React.CSSProperties}>
              <div className="category-card__icon">{cat.icon}</div>
              <div className="category-card__body">
                <h3 className="category-card__title">{cat.title}</h3>
                <p className="category-card__desc">{cat.description}</p>
              </div>
              <span className="category-card__count">{cat.count}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Quick Reference */}
      <section className="quick-ref">
        <h2 className="section-title">Quick Reference</h2>
        <div className="quick-ref__grid">
          {quickLinks.map((link) => (
            <Link key={link.url} to={link.url} className="quick-ref-card">
              <h3 className="quick-ref-card__title">{link.title}</h3>
              <p className="quick-ref-card__desc">{link.description}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* External Resources */}
      <section className="external-links">
        <h2 className="section-title">External Resources</h2>
        <div className="external-links__list">
          {externalLinks.map((link) => (
            <a key={link.url} href={link.url} target="_blank" rel="noopener noreferrer" className="external-link">
              <span className="external-link__title">{link.title}</span>
              <span className="external-link__desc">{link.desc}</span>
              <span className="external-link__arrow">↗</span>
            </a>
          ))}
        </div>
      </section>
    </div>
  )
}
