import fs from 'node:fs'
import path from 'node:path'

const dir = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1'))
const enPath = path.join(dir, 'en.ts')
const jaPath = path.join(dir, 'ja.ts')
const esPath = path.join(dir, 'es.ts')

const en = fs.readFileSync(enPath, 'utf8')
const ja = fs.readFileSync(jaPath, 'utf8')

// Build ordered list of English string literals (simple quoted strings only)
function extractQuotedStrings(source) {
  const results = []
  const re = /:\s*'((?:\\'|[^'])*)'/g
  let m
  while ((m = re.exec(source)) !== null) {
    results.push(m[1].replace(/\\'/g, "'"))
  }
  return results
}

const enStrings = extractQuotedStrings(en)
const jaStrings = extractQuotedStrings(ja)

console.log(`en: ${enStrings.length}, ja: ${jaStrings.length}`)
