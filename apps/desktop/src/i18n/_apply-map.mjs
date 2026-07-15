import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const map = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-map.json'), 'utf8'))

let body = fs.readFileSync(path.join(__dirname, 'es.ts'), 'utf8')
const entries = Object.entries(map).sort((a, b) => b[0].length - a[0].length)
for (const [en, es] of entries) {
  if (!en || en === es) continue
  const escapedEn = en.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const escapedEs = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  body = body.split(`'${escapedEn}'`).join(`'${escapedEs}'`)
}

fs.writeFileSync(path.join(__dirname, 'es.ts'), body, 'utf8')
const remaining = [...body.matchAll(/:\s*'([A-Za-z][^']{2,})'/g)].filter(m => /[A-Za-z]{3,}/.test(m[1])).length
console.log('applied map, rough remaining english-ish literals:', remaining)
