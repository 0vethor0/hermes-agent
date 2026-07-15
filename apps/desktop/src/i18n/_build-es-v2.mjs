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
    if (openMatch) {
      stack.push({ indent, key: openMatch[2].replace(/^'|'$/g, '') })
    }
  }
  return map
}

const jaMap = extractJaByKeyPath(fs.readFileSync(path.join(__dirname, 'ja.ts'), 'utf8'))

// Spanish translations keyed by English string
const esByEn = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-manual.json'), 'utf8'))

// Merge pairs: ensure every en from keypaths has Spanish (fallback keeps en)
for (const { keyPath, en } of pairs) {
  if (!esByEn[en] || esByEn[en] === en) {
    // keep existing or mark for manual pass
  }
}

let body = fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8')
body = body.replace(
  /^import[\s\S]*?export const en: Translations = \{\r?\n/,
  `import { defineFieldCopy } from '@/app/settings/field-copy'\n\nimport { defineLocale } from './define-locale'\n\nexport const es = defineLocale({\n`
)
body = body.replace(/\r?\n\}\s*$/, '\n})\n')
body = body.replace(
  /    fieldLabels: FIELD_LABELS,\r?\n    fieldDescriptions: FIELD_DESCRIPTIONS,/,
  fs.readFileSync(path.join(__dirname, '_field-copy-es.txt'), 'utf8').trim()
)

const jaToEs = {}
for (const [keyPath, ja] of jaMap) {
  const enPair = pairs.find(p => p.keyPath === keyPath)
  if (!enPair) continue
  const es = esByEn[enPair.en] ?? enPair.en
  jaToEs[ja] = es
}

const allEntries = [
  ...Object.entries(esByEn),
  ...Object.entries(jaToEs)
].sort((a, b) => b[0].length - a[0].length)

for (const [from, to] of allEntries) {
  if (!from || from === to) continue
  const escapedFrom = from.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const escapedTo = to.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  body = body.split(`'${escapedFrom}'`).join(`'${escapedTo}'`)
}

fs.writeFileSync(path.join(__dirname, 'es.ts'), body, 'utf8')
const englishLeft = [...body.matchAll(/:\s*'([A-Za-z][^']{4,})'/g)].length
const japaneseLeft = (body.match(/[\u3040-\u30ff\u4e00-\u9fff]/g) || []).length
console.log({ englishLeft, japaneseLeft, lines: body.split('\n').length })
