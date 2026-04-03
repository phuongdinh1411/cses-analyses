export interface FrontMatter {
  title?: string
  layout?: string
  permalink?: string
  difficulty?: string
  tags?: string[]
  [key: string]: unknown
}

export interface ParsedMarkdown {
  frontMatter: FrontMatter
  content: string
}

export function parseFrontMatter(raw: string): ParsedMarkdown {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/)
  if (!match) {
    return { frontMatter: {}, content: raw }
  }

  const yamlBlock = match[1]
  const content = match[2]
  const frontMatter: FrontMatter = {}

  for (const line of yamlBlock.split('\n')) {
    const colonIdx = line.indexOf(':')
    if (colonIdx === -1) continue
    const key = line.slice(0, colonIdx).trim()
    let value = line.slice(colonIdx + 1).trim()

    // Remove surrounding quotes
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1)
    }

    // Handle arrays like [math, xor, array]
    if (value.startsWith('[') && value.endsWith(']')) {
      frontMatter[key] = value.slice(1, -1).split(',').map(s => s.trim())
    } else {
      frontMatter[key] = value
    }
  }

  return { frontMatter, content }
}
