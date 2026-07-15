import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

function extractQuotedStrings(source) {
  const results = []
  const re = /:\s*'((?:\\'|[^'])*)'/g
  let m
  while ((m = re.exec(source)) !== null) {
    results.push(m[1].replace(/\\'/g, "'"))
  }
  return results
}

const en = extractQuotedStrings(fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8'))
const zh = extractQuotedStrings(fs.readFileSync(path.join(__dirname, 'zh.ts'), 'utf8'))
const ja = extractQuotedStrings(fs.readFileSync(path.join(__dirname, 'ja.ts'), 'utf8'))
console.log({ en: en.length, zh: zh.length, ja: ja.length })
