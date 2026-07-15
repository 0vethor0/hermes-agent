import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const enText = fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8')
const jaText = fs.readFileSync(path.join(__dirname, 'ja.ts'), 'utf8')

function extractQuotedStrings(source) {
  const results = []
  const re = /:\s*'((?:\\'|[^'])*)'/g
  let m
  while ((m = re.exec(source)) !== null) {
    results.push(m[1].replace(/\\'/g, "'"))
  }
  return results
}

const enStrings = extractQuotedStrings(enText)
const jaStrings = extractQuotedStrings(jaText)

// Spanish translations aligned to en strings (by index where ja exists, else keep en for manual follow-up)
const esStrings = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-strings-array.json'), 'utf8'))

if (esStrings.length !== enStrings.length) {
  console.error(`Length mismatch: en=${enStrings.length} es=${esStrings.length}`)
  process.exit(1)
}

const map = Object.fromEntries(enStrings.map((s, i) => [s, esStrings[i]]))
fs.writeFileSync(path.join(__dirname, '_es-map.json'), JSON.stringify(map, null, 2), 'utf8')
console.log('map entries', Object.keys(map).length)
