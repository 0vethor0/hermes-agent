import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const pairs = JSON.parse(fs.readFileSync(path.join(__dirname, '_keypath-pairs.json'), 'utf8'))

// Load base map from heuristic generator if present
let baseMap = {}
try {
  baseMap = JSON.parse(fs.readFileSync(path.join(__dirname, '_es-map.json'), 'utf8'))
} catch {}

const manual = {
  Apply: 'Aplicar',
  Back: 'Atrás',
  Save: 'Guardar',
  'Saving…': 'Guardando…',
  Cancel: 'Cancelar',
  Change: 'Cambiar',
  Choose: 'Elegir',
  Clear: 'Limpiar',
  Close: 'Cerrar',
  Collapse: 'Contraer',
  Confirm: 'Confirmar',
  Connect: 'Conectar',
  Connecting: 'Conectando',
  Continue: 'Continuar',
  Copied: 'Copiado',
  Copy: 'Copiar',
  'Copy failed': 'Error al copiar',
  Delete: 'Eliminar',
  Docs: 'Documentación',
  Done: 'Listo',
  Error: 'Error',
  Expand: 'Expandir',
  Failed: 'Fallido',
  'Format JSON': 'Formatear JSON',
  Free: 'Gratis',
  'Loading…': 'Cargando…',
  'Not set': 'Sin configurar',
  Refresh: 'Actualizar',
  Remove: 'Eliminar',
  Replace: 'Reemplazar',
  Retry: 'Reintentar',
  Run: 'Ejecutar',
  Send: 'Enviar',
  Set: 'Establecer',
  Skip: 'Omitir',
  Update: 'Actualizar',
  On: 'Activado',
  Off: 'Desactivado',
  'Reveal in Finder': 'Mostrar en Finder',
  'Reveal in File Explorer': 'Mostrar en el Explorador de archivos',
  'Open Containing Folder': 'Abrir carpeta contenedora',
  'Reveal in filetree': 'Mostrar en el árbol de archivos',
  'Copy Path': 'Copiar ruta',
  'Copy Relative Path': 'Copiar ruta relativa',
  'Rename…': 'Renombrar…',
  'New name': 'Nuevo nombre',
  'It will be moved to the Trash — you can restore it from there.':
    'Se moverá a la papelera; puedes restaurarlo desde ahí.',
  'Path copied': 'Ruta copiada',
  'Hermes Desktop is ready': 'Hermes Desktop está listo',
  'Connecting live desktop gateway': 'Conectando al gateway de escritorio en vivo',
  'Loading Hermes settings': 'Cargando configuración de Hermes',
  'Loading recent sessions': 'Cargando sesiones recientes',
  'Starting desktop connection': 'Iniciando conexión de escritorio',
  'Starting Hermes Desktop…': 'Iniciando Hermes Desktop…',
  'Hermes background process exited.': 'El proceso en segundo plano de Hermes finalizó.',
  'Hermes background process exited during startup.':
    'El proceso en segundo plano de Hermes finalizó durante el inicio.',
  'Backend stopped': 'Backend detenido',
  'Desktop boot failed': 'Error al iniciar el escritorio',
  'Lost connection to the gateway': 'Se perdió la conexión con el gateway',
  'Gateway sign-in required': 'Se requiere iniciar sesión en el gateway',
  'Desktop IPC bridge is unavailable.': 'El puente IPC de escritorio no está disponible.',
  "Hermes couldn't start": 'No se pudo iniciar Hermes',
  'Remote gateway sign-in required': 'Se requiere iniciar sesión en el gateway remoto',
  'Your remote gateway session has expired. Sign in again to reconnect. Nothing here deletes your chats or settings.':
    'Tu sesión del gateway remoto expiró. Inicia sesión de nuevo para reconectar. Nada aquí elimina tus chats ni tu configuración.',
  'Repair install': 'Reparar instalación',
  'Use local gateway': 'Usar gateway local',
  'Gateway settings': 'Configuración del gateway',
  'Repair re-runs the installer and can take a few minutes on a fresh machine.':
    'La reparación vuelve a ejecutar el instalador y puede tardar unos minutos en una máquina nueva.',
  'Sign out & sign in': 'Cerrar sesión e iniciar sesión',
  'Check the gateway URL and sign-in under Gateway settings, or switch to the local gateway.':
    'Revisa la URL del gateway y el inicio de sesión en Configuración del gateway, o cambia al gateway local.',
  'Hide recent logs': 'Ocultar registros recientes',
  'Show recent logs': 'Mostrar registros recientes',
  'Signed in': 'Sesión iniciada',
  'Reconnecting to the remote gateway…': 'Reconectando al gateway remoto…',
  'Sign-in incomplete': 'Inicio de sesión incompleto',
  'The login window closed before authentication finished.':
    'La ventana de inicio de sesión se cerró antes de completar la autenticación.',
  'Sign-in failed': 'Error al iniciar sesión',
  'Sign in to remote gateway': 'Iniciar sesión en el gateway remoto',
  'your identity provider': 'tu proveedor de identidad',
  Notifications: 'Notificaciones',
  Hide: 'Ocultar',
  Show: 'Mostrar',
  'Clear all': 'Limpiar todo',
  'Dismiss notification': 'Descartar notificación',
  Details: 'Detalles',
  'Copy detail': 'Copiar detalle',
  'Could not copy notification detail': 'No se pudo copiar el detalle de la notificación',
  'Backend out of date': 'Backend desactualizado',
  'Unsupported install method': 'Método de instalación no compatible',
  'Update Hermes': 'Actualizar Hermes',
  'Update ready': 'Actualización lista',
  "See what's new": 'Ver novedades',
  'Keyboard shortcuts': 'Atajos de teclado',
  Rebind: 'Reasignar',
  'Reset to default': 'Restablecer predeterminado',
  'Reset all': 'Restablecer todo',
  'Press a key…': 'Pulsa una tecla…',
  set: 'asignado',
  Language: 'Idioma',
  'Choose the language for the desktop interface.': 'Elige el idioma de la interfaz de escritorio.',
  'Saving language…': 'Guardando idioma…',
  'Language update failed': 'Error al actualizar el idioma',
  'Switch language': 'Cambiar idioma',
  'Search languages…': 'Buscar idiomas…',
  'No languages found': 'No se encontraron idiomas',
  'Close settings': 'Cerrar configuración',
  'Export config': 'Exportar configuración',
  'Import config': 'Importar configuración',
  'Reset to defaults': 'Restablecer valores predeterminados',
  'Reset all settings to Hermes defaults?': '¿Restablecer toda la configuración a los valores predeterminados de Hermes?',
  Providers: 'Proveedores',
  Accounts: 'Cuentas',
  'API keys': 'Claves API',
  'Tools & Keys': 'Herramientas y claves',
  Tools: 'Herramientas',
  Settings: 'Configuración',
  'Archived Chats': 'Chats archivados',
  About: 'Acerca de',
  Sessions: 'Sesiones',
  Gateway: 'Gateway',
  Messaging: 'Mensajería',
  Artifacts: 'Artefactos',
  Profiles: 'Perfiles',
  Composer: 'Compositor',
  Navigation: 'Navegación',
  View: 'Vista',
  Session: 'Sesión',
  Cron: 'Cron',
  Agents: 'Agentes',
  Maintenance: 'Mantenimiento',
  System: 'Sistema',
  Usage: 'Uso',
  Appearance: 'Apariencia',
  Advanced: 'Avanzado',
  Memory: 'Memoria',
  Voice: 'Voz',
  Safety: 'Seguridad',
  Workspace: 'Espacio de trabajo',
  Chat: 'Chat',
  Model: 'Modelo',
  Search: 'Buscar',
  Install: 'Instalar',
  Preview: 'Vista previa',
  Terminal: 'Terminal',
  Local: 'Local',
  Remote: 'Remoto',
  Email: 'Correo',
  Name: 'Nombre',
  Prompt: 'Prompt',
  Optional: 'Opcional',
  Enabled: 'Habilitado',
  Disabled: 'Deshabilitado',
  Connected: 'Conectado',
  Disconnected: 'Desconectado',
  Running: 'En ejecución',
  Stopped: 'Detenido',
  Starting: 'Iniciando',
  Failed: 'Fallido',
  Done: 'Listo',
  Copy: 'Copiar',
  Edit: 'Editar',
  Rename: 'Renombrar',
  Archive: 'Archivar',
  Export: 'Exportar',
  Import: 'Importar',
  Test: 'Probar',
  Save: 'Guardar',
  Cancel: 'Cancelar',
  Delete: 'Eliminar',
  Close: 'Cerrar',
  Open: 'Abrir',
  Back: 'Atrás',
  Continue: 'Continuar',
  Retry: 'Reintentar',
  Refresh: 'Actualizar',
  Loading: 'Cargando',
  None: 'Ninguno',
  All: 'Todos',
  General: 'General',
  Recommended: 'Recomendado',
  Required: 'Requerido',
  Unknown: 'Desconocido',
  Pro: 'Pro',
  Free: 'Gratis',
  Input: 'Entrada',
  Output: 'Salida',
  Total: 'Total',
  Tokens: 'Tokens',
  Logs: 'Registros',
  Status: 'Estado',
  Actions: 'Acciones',
  Documentation: 'Documentación',
  'Command palette': 'Paleta de comandos',
  'Command Center': 'Centro de comandos',
  'Memory Graph': 'Grafo de memoria',
  'New session': 'Nueva sesión',
  'Scheduled jobs': 'Tareas programadas',
  'Something went wrong': 'Algo salió mal',
  'Reload window': 'Recargar ventana',
  Sidebar: 'Barra lateral',
  'Toggle Sidebar': 'Alternar barra lateral',
  'Clear search': 'Limpiar búsqueda',
  pagination: 'paginación',
  Prev: 'Ant.',
  Next: 'Sig.'
}

function translate(en) {
  if (manual[en]) return manual[en]
  if (baseMap[en] && baseMap[en] !== en) return baseMap[en]
  return en
}

const enToEs = {}
const zhToEs = {}
for (const { en, zh } of pairs) {
  const es = translate(en)
  enToEs[en] = es
  if (zh) zhToEs[zh] = es
}

fs.writeFileSync(path.join(__dirname, '_es-manual.json'), JSON.stringify(enToEs, null, 2), 'utf8')
fs.writeFileSync(path.join(__dirname, '_zh-to-es.json'), JSON.stringify(zhToEs, null, 2), 'utf8')

let zhBody = fs.readFileSync(path.join(__dirname, 'zh.ts'), 'utf8')
zhBody = zhBody.replace(
  /^import[\s\S]*?export const zh: Translations = \{\n/,
  `import { defineFieldCopy } from '@/app/settings/field-copy'\n\nimport { defineLocale } from './define-locale'\n\nexport const es = defineLocale({\n`
)
zhBody = zhBody.replace(/\n\}\s*$/, '\n})\n')
zhBody = zhBody.replace(
  /    fieldLabels: defineFieldCopy\([\s\S]*?\),\n    fieldDescriptions: defineFieldCopy\([\s\S]*?\),/,
  fs.readFileSync(path.join(__dirname, '_field-copy-es.txt'), 'utf8').trim()
)

const entries = Object.entries(zhToEs).sort((a, b) => b[0].length - a[0].length)
for (const [zh, es] of entries) {
  if (!zh || zh === es) continue
  const escapedZh = zh.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const escapedEs = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  zhBody = zhBody.split(`'${escapedZh}'`).join(`'${escapedEs}'`)
}

// Also apply remaining en strings that might still be in file (English leftovers in zh)
const enEntries = Object.entries(enToEs).sort((a, b) => b[0].length - a[0].length)
for (const [en, es] of enEntries) {
  if (!en || en === es) continue
  const escapedEn = en.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  const escapedEs = es.replace(/\\/g, '\\\\').replace(/'/g, "\\'")
  zhBody = zhBody.split(`'${escapedEn}'`).join(`'${escapedEs}'`)
}

fs.writeFileSync(path.join(__dirname, 'es.ts'), zhBody, 'utf8')
const chineseLeft = (zhBody.match(/[\u4e00-\u9fff]/g) || []).length
console.log({ pairs: pairs.length, enToEs: Object.keys(enToEs).length, chineseLeft })
