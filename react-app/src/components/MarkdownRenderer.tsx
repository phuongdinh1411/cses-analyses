import React, { useState, useCallback, useMemo } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import rehypeRaw from 'rehype-raw'
import rehypeSlug from 'rehype-slug'
import type { Components } from 'react-markdown'
import MermaidBlock from './MermaidBlock'

// No highlight.js theme import — we use a custom Catppuccin Mocha palette in App.css

interface MarkdownRendererProps {
  content: string
}

// Language display names
const LANG_NAMES: Record<string, string> = {
  py: 'Python', python: 'Python',
  js: 'JavaScript', javascript: 'JavaScript',
  ts: 'TypeScript', typescript: 'TypeScript',
  jsx: 'JSX', tsx: 'TSX',
  java: 'Java', cpp: 'C++', 'c++': 'C++', c: 'C',
  go: 'Go', rust: 'Rust', rb: 'Ruby', ruby: 'Ruby',
  sh: 'Shell', bash: 'Bash', zsh: 'Shell',
  sql: 'SQL', html: 'HTML', css: 'CSS',
  json: 'JSON', yaml: 'YAML', yml: 'YAML',
  xml: 'XML', md: 'Markdown', markdown: 'Markdown',
  text: 'Text', txt: 'Text',
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement('textarea')
      textarea.value = text
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }, [text])

  return (
    <button
      className={`code-block-copy${copied ? ' code-block-copy--copied' : ''}`}
      onClick={handleCopy}
      aria-label={copied ? 'Copied' : 'Copy code'}
    >
      {copied ? (
        <>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          Copied
        </>
      ) : (
        <>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
          </svg>
          Copy
        </>
      )}
    </button>
  )
}

// Extract plain text from a React element tree (handles rehype-highlight spans)
function extractTextFromChildren(node: React.ReactNode): string {
  if (typeof node === 'string') return node
  if (typeof node === 'number') return String(node)
  if (!node) return ''
  if (Array.isArray(node)) return node.map(extractTextFromChildren).join('')
  if (typeof node === 'object' && 'props' in node) {
    return extractTextFromChildren((node as React.ReactElement<{ children?: React.ReactNode }>).props.children)
  }
  return ''
}

// Tabbed code group: renders code blocks as tabs.
// Languages are passed via data-languages on the marker div (set by groupCodeBlocks).
function CodeTabGroup({ languages, children }: { languages: string[]; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(0)

  // Convert children to an array of React nodes (one per code-block-wrapper)
  const blocks = useMemo(() => {
    const arr: React.ReactNode[] = []
    React.Children.forEach(children, (child) => {
      if (React.isValidElement(child)) arr.push(child)
    })
    return arr
  }, [children])

  if (blocks.length <= 1) {
    return <>{children}</>
  }

  // Build tab data from hardcoded languages + block elements
  const tabs = languages.slice(0, blocks.length).map((lang, i) => ({
    lang,
    displayLang: LANG_NAMES[lang] || lang || 'Code',
    element: blocks[i],
  }))

  // Extract code text from the active tab's block for copy button
  const activeCodeText = useMemo(() => {
    const block = blocks[activeTab]
    if (!block || !React.isValidElement(block)) return ''
    // block is <div class="code-block-wrapper"><div class="code-block-header">...</div><pre><code>...</code></pre></div>
    // Walk into pre > code to get text
    return extractTextFromChildren(block).replace(/\n$/, '')
  }, [blocks, activeTab])

  return (
    <div className="code-tab-group">
      <div className="code-tab-bar">
        {tabs.map((tab, i) => (
          <button
            key={tab.lang + i}
            className={`code-tab-btn${i === activeTab ? ' code-tab-btn--active' : ''}`}
            onClick={() => setActiveTab(i)}
          >
            {tab.displayLang}
          </button>
        ))}
        {activeCodeText && (
          <div className="code-tab-copy">
            <CopyButton text={activeCodeText} />
          </div>
        )}
      </div>
      <div className="code-tab-panel">
        {tabs[activeTab]?.element}
      </div>
    </div>
  )
}

// Custom components for react-markdown
const components: Components = {
  // Wrap <pre> blocks with language label + copy button
  pre({ children, ...props }) {
    // Extract language and text from the child <code> element
    let language = ''
    let codeText = ''

    if (children && typeof children === 'object' && 'props' in (children as any)) {
      const codeProps = (children as any).props
      const classMatch = /language-(\w+)/.exec(codeProps?.className || '')
      language = classMatch ? classMatch[1] : ''
      // Extract raw text for copy
      codeText = String(codeProps?.children || '').replace(/\n$/, '')
    }

    // Don't wrap mermaid blocks
    if (language === 'mermaid') {
      return <pre {...props}>{children}</pre>
    }

    const displayLang = LANG_NAMES[language] || language

    return (
      <div className="code-block-wrapper">
        <div className="code-block-header">
          <span className="code-block-lang">{displayLang}</span>
          {codeText && <CopyButton text={codeText} />}
        </div>
        <pre {...props}>{children}</pre>
      </div>
    )
  },
  // Intercept code blocks to handle Mermaid
  code({ className, children, ...props }) {
    const match = /language-(\w+)/.exec(className || '')
    const language = match ? match[1] : ''

    // Mermaid diagram
    if (language === 'mermaid') {
      return <MermaidBlock chart={String(children).replace(/\n$/, '')} />
    }

    // Regular inline code or code block (rehype-highlight handles block syntax)
    return (
      <code className={className} {...props}>
        {children}
      </code>
    )
  },
  // Render tabbed code groups from our preprocessing markers
  div({ className, children, ...props }) {
    if (className === 'code-tab-group-marker') {
      const languages = ((props as Record<string, unknown>)['data-languages'] as string || '').split(',').filter(Boolean)
      return <CodeTabGroup languages={languages}>{children}</CodeTabGroup>
    }
    return <div className={className} {...props}>{children}</div>
  },
  // Make links open in new tab for external URLs
  a({ href, children, ...props }) {
    const isExternal = href?.startsWith('http')
    return (
      <a
        href={href}
        {...(isExternal ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
        {...props}
      >
        {children}
      </a>
    )
  },
}

// Preprocess markdown to wrap consecutive code blocks in tab group markers.
// Detects 2+ fenced code blocks in different languages separated only by blank lines.
function groupCodeBlocks(md: string): string {
  // Match fenced code blocks: ```lang\n...\n```
  const codeBlockRe = /```(\w+)\n[\s\S]*?\n```/g
  const blocks: { start: number; end: number; lang: string }[] = []
  let match
  while ((match = codeBlockRe.exec(md)) !== null) {
    blocks.push({ start: match.index, end: match.index + match[0].length, lang: match[1] })
  }

  if (blocks.length < 2) return md

  // Find groups of consecutive code blocks separated by only whitespace
  const groups: { start: number; end: number; blockIndices: number[] }[] = []
  let i = 0
  while (i < blocks.length) {
    const group = [i]
    let j = i + 1
    while (j < blocks.length) {
      const between = md.slice(blocks[j - 1].end, blocks[j].start)
      // Only group if separated by blank lines (no other content) and different languages
      if (between.trim() === '') {
        // Check the group would have distinct languages
        const langs = new Set(group.map(idx => blocks[idx].lang))
        if (!langs.has(blocks[j].lang)) {
          group.push(j)
          j++
          continue
        }
      }
      break
    }
    if (group.length >= 2) {
      groups.push({
        start: blocks[group[0]].start,
        end: blocks[group[group.length - 1]].end,
        blockIndices: group,
      })
    }
    i = group.length >= 2 ? j : i + 1
  }

  if (groups.length === 0) return md

  // Build result by replacing groups with wrapped versions (process from end to preserve offsets)
  let result = md
  for (let g = groups.length - 1; g >= 0; g--) {
    const group = groups[g]
    const content = result.slice(group.start, group.end)
    const langs = group.blockIndices.map(idx => blocks[idx].lang).join(',')
    const wrapped = `<div class="code-tab-group-marker" data-languages="${langs}">\n\n${content}\n\n</div>`
    result = result.slice(0, group.start) + wrapped + result.slice(group.end)
  }

  return result
}

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const processed = useMemo(() => groupCodeBlocks(content), [content])

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw, rehypeSlug, rehypeHighlight]}
      components={components}
    >
      {processed}
    </ReactMarkdown>
  )
}
