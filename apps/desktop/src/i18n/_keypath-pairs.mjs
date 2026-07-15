import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

function extractByKeyPath(source) {
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
    if (openMatch) {
      const key = openMatch[2].replace(/^'|'$/g, '')
      stack.push({ indent, key })
    }
  }

  return map
}

const enMap = extractByKeyPath(fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8'))
const zhMap = extractByKeyPath(fs.readFileSync(path.join(__dirname, 'zh.ts'), 'utf8'))
console.log({ en: enMap.size, zh: zhMap.size })

const pairs = []
for (const [keyPath, en] of enMap) {
  if (zhMap.has(keyPath)) pairs.push({ keyPath, en, zh: zhMap.get(keyPath) })
}
console.log('paired', pairs.length)
fs.writeFileSync(path.join(__dirname, '_keypath-pairs.json'), JSON.stringify(pairs, null, 2))
