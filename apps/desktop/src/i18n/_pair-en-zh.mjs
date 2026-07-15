import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

function extractPairs(source) {
  const pairs = []
  const re = /^\s*([A-Za-z0-9_.'-]+|'[^']+'):\s*'((?:\\'|[^'])*)'/gm
  let m
  while ((m = re.exec(source)) !== null) {
    pairs.push({ key: m[1], value: m[2].replace(/\\'/g, "'") })
  }
  return pairs
}

const enPairs = extractPairs(fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8'))
const zhPairs = extractPairs(fs.readFileSync(path.join(__dirname, 'zh.ts'), 'utf8'))
console.log({ en: enPairs.length, zh: zhPairs.length })

const aligned = []
for (let i = 0; i < Math.min(enPairs.length, zhPairs.length); i++) {
  if (enPairs[i].key !== zhPairs[i].key) {
    console.warn('key mismatch', i, enPairs[i].key, zhPairs[i].key)
  }
  aligned.push({ key: enPairs[i].key, en: enPairs[i].value, zh: zhPairs[i].value })
}
fs.writeFileSync(path.join(__dirname, '_aligned-pairs.json'), JSON.stringify(aligned, null, 2))
console.log('wrote aligned pairs', aligned.length)
