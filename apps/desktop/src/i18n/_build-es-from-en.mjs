import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const header = `import { defineFieldCopy } from '@/app/settings/field-copy'

import { defineLocale } from './define-locale'

export const es = defineLocale(
`

const footer = `
)
`

// Load pre-translated body: start from en.ts, strip header/footer, wrap in defineLocale
let body = fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8')
body = body.replace(/^import[\s\S]*?export const en: Translations = \{\n/, '')
body = body.replace(/\n\}\s*$/, '\n')

// Replace field labels block
body = body.replace(
  /    fieldLabels: FIELD_LABELS,\n    fieldDescriptions: FIELD_DESCRIPTIONS,/,
  fs.readFileSync(path.join(__dirname, '_field-copy-es.txt'), 'utf8').trim()
)

// Apply string translations from map
const map = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-map.json'), 'utf8'))

for (const [en, es] of Object.entries(map)) {
  if (en === es) continue
  const escaped = en.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const replacement = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  body = body.split(`'${escaped}'`).join(`'${replacement}'`)
}

fs.writeFileSync(path.join(__dirname, 'es.ts'), header + body + footer, 'utf8')
console.log('Wrote es.ts')
