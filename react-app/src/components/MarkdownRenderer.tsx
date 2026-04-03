import { useState, useCallback } from 'react'
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

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw, rehypeSlug, rehypeHighlight]}
      components={components}
    >
      {content}
    </ReactMarkdown>
  )
}
