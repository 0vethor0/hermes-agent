import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const pairs = JSON.parse(fs.readFileSync(path.join(__dirname, '_keypath-pairs.json'), 'utf8'))

function extractJaByKeyPath(source) {
  const lines = source.split('\n')
  const stack = []
  const map = new Map()
  for (const line of lines) {
    const indent = line.match(/^(\s*)/)[1].length
    while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop()
    const keyMatch = line.match(/^(\s*)([A-Za-z0-9_.'-]+|'[^']+'):\s*'((?:\\'|[^'])*)'/)
    if (keyMatch) {
      const key = keyMatch[2].replace(/^'|'$/g, '')
      const value = keyMatch[3].replace(/\\'/g, "'")
      const pathParts = stack.map(s => s.key)
      pathParts.push(key)
      map.set(pathParts.join('.'), value)
      continue
    }
    const openMatch = line.match(/^(\s*)([A-Za-z0-9_.'-]+|'[^']+'):\s*\{/)
    if (openMatch) stack.push({ indent, key: openMatch[2].replace(/^'|'$/g, '') })
  }
  return map
}

const jaMap = extractJaByKeyPath(fs.readFileSync(path.join(__dirname, 'ja.ts'), 'utf8'))
const existing = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-manual.json'), 'utf8'))

// For each pair, if still English, use ja string as placeholder marker for untranslated
const missing = []
for (const { keyPath, en } of pairs) {
  if (!existing[en] || existing[en] === en) missing.push({ keyPath, en, ja: jaMap.get(keyPath) })
}
fs.writeFileSync(path.join(__dirname, '_missing-translations.json'), JSON.stringify(missing, null, 2))
console.log('missing', missing.length)
