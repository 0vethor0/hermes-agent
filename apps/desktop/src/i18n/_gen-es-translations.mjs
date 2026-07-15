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
console.log(JSON.stringify({ en: enStrings.length, ja: jaStrings.length, diff: enStrings.length - jaStrings.length }, null, 2))
