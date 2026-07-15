import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const enText = fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8')

function extractQuotedStrings(source) {
  const results = []
  const re = /:\s*'((?:\\'|[^'])*)'/g
  let m
  while ((m = re.exec(source)) !== null) {
    results.push(m[1].replace(/\\'/g, "'"))
  }
  return results
}

const unique = [...new Set(extractQuotedStrings(enText))].sort()
fs.writeFileSync(path.join(__dirname, '_en-strings.json'), JSON.stringify(unique, null, 2), 'utf8')
console.log('unique strings:', unique.length)
