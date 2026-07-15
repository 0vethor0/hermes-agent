import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Manual high-quality Spanish overrides keyed by exact English source string.
// Generated sections are merged on top of heuristic fallbacks.
const manual = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-manual.json'), 'utf8'))

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function applyMap(source, map) {
  let out = source
  const entries = Object.entries(map).sort((a, b) => b[0].length - a[0].length)
  for (const [en, es] of entries) {
    if (!en || en === es) continue
    const escapedEn = en.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
    const escapedEs = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
    out = out.split(`'${escapedEn}'`).join(`'${escapedEs}'`)
  }
  return out
}

let body = fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8')
body = body.replace(/^import[\s\S]*?export const en: Translations = \{\n/, '')
body = body.replace(/\n\}\s*$/, '\n')

body = body.replace(
  /    fieldLabels: FIELD_LABELS,\n    fieldDescriptions: FIELD_DESCRIPTIONS,/,
  fs.readFileSync(path.join(__dirname, '_field-copy-es.txt'), 'utf8').trim()
)

body = applyMap(body, manual)

const header = `import { defineFieldCopy } from '@/app/settings/field-copy'

import { defineLocale } from './define-locale'

export const es = defineLocale({
`

fs.writeFileSync(path.join(__dirname, 'es.ts'), `${header}${body}\n})\n`, 'utf8')
console.log('built es.ts')
