import { useEffect, useRef, useId } from 'react'
import mermaid from 'mermaid'

// Initialize mermaid once
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis',
  },
})

interface MermaidBlockProps {
  chart: string
}

export default function MermaidBlock({ chart }: MermaidBlockProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const id = useId().replace(/:/g, '_')

  useEffect(() => {
    if (!containerRef.current || !chart.trim()) return

    let cancelled = false

    async function render() {
      try {
        const { svg } = await mermaid.render(`mermaid-${id}`, chart.trim())
        if (!cancelled && containerRef.current) {
          containerRef.current.innerHTML = svg
        }
      } catch {
        // If mermaid fails, show the raw text
        if (!cancelled && containerRef.current) {
          containerRef.current.textContent = chart
        }
      }
    }

    render()

    return () => {
      cancelled = true
    }
  }, [chart, id])

  return <div ref={containerRef} className="mermaid-container" />
}
