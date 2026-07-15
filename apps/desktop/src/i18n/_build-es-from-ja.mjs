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
    if (openMatch) stack.push({ indent, key: openMatch[2].replace(/^'|'$/g, '') })
  }
  return map
}

const enMap = extractByKeyPath(fs.readFileSync(path.join(__dirname, 'en.ts'), 'utf8'))
const jaMap = extractByKeyPath(fs.readFileSync(path.join(__dirname, 'ja.ts'), 'utf8'))
const manual = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-manual.json'), 'utf8'))

const jaToEs = {}
for (const [keyPath, en] of enMap) {
  const ja = jaMap.get(keyPath)
  if (!ja) continue
  const es = manual[en] ?? en
  jaToEs[ja] = es
}

let body = fs.readFileSync(path.join(__dirname, 'ja.ts'), 'utf8')
body = body.replace(
  /^import[\s\S]*?export const ja = defineLocale\(\{\r?\n/,
  `import { defineFieldCopy } from '@/app/settings/field-copy'\n\nimport { defineLocale } from './define-locale'\n\nexport const es = defineLocale({\n`
)
body = body.replace(/\r?\n\}\)\s*$/, '\n})\n')
body = body.replace(
  /    fieldLabels: defineFieldCopy\([\s\S]*?\),\n    fieldDescriptions: defineFieldCopy\([\s\S]*?\),/,
  fs.readFileSync(path.join(__dirname, '_field-copy-es.txt'), 'utf8').trim()
)

const entries = Object.entries(jaToEs).sort((a, b) => b[0].length - a[0].length)
for (const [ja, es] of entries) {
  if (!ja || ja === es) continue
  const escapedJa = ja.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const escapedEs = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  body = body.split(`'${escapedJa}'`).join(`'${escapedEs}'`)
}

// Apply direct en->es for any English leftovers in ja file
const enEntries = Object.entries(manual).sort((a, b) => b[0].length - a[0].length)
for (const [en, es] of enEntries) {
  if (!en || en === es) continue
  const escapedEn = en.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const escapedEs = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  body = body.split(`'${escapedEn}'`).join(`'${escapedEs}'`)
}

// Patch known Spanish sections from high-quality manual translations
const highQuality = {
  apply: 'Aplicar',
  back: 'Atrás',
  save: 'Guardar',
  saving: 'Guardando…',
  cancel: 'Cancelar',
  change: 'Cambiar',
  choose: 'Elegir',
  clear: 'Limpiar',
  close: 'Cerrar',
  collapse: 'Contraer',
  confirm: 'Confirmar',
  connect: 'Conectar',
  connecting: 'Conectando',
  continue: 'Continuar',
  copied: 'Copiado',
  copy: 'Copiar',
  copyFailed: 'Error al copiar',
  delete: 'Eliminar',
  docs: 'Documentación',
  done: 'Listo',
  expand: 'Expandir',
  failed: 'Fallido',
  formatJson: 'Formatear JSON',
  free: 'Gratis',
  loading: 'Cargando…',
  notSet: 'Sin configurar',
  refresh: 'Actualizar',
  remove: 'Eliminar',
  replace: 'Reemplazar',
  retry: 'Reintentar',
  run: 'Ejecutar',
  send: 'Enviar',
  set: 'Establecer',
  skip: 'Omitir',
  update: 'Actualizar',
  on: 'Activado',
  off: 'Desactivado'
}
for (const [k, v] of Object.entries(highQuality)) {
  body = body.replace(new RegExp(`(${k}:\\s*)'[^']*'`), `$1'${v}'`)
}

fs.writeFileSync(path.join(__dirname, 'es.ts'), body, 'utf8')
const japaneseLeft = (body.match(/[\u3040-\u30ff\u4e00-\u9fff]/g) || []).length
const englishLeft = [...body.matchAll(/:\s*'([A-Za-z][^']{4,})'/g)].length
console.log({ jaToEs: Object.keys(jaToEs).length, japaneseLeft, englishLeft, lines: body.split('\n').length })
