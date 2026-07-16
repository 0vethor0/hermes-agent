import React, { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n'
import { triggerHaptic } from '@/lib/haptics'
import { Mic, Loader2 } from '@/lib/icons'
import { ListRow } from './primitives'

export function AcouzSettingsPanel() {
  const { t } = useI18n()
  const [isRunning, setIsRunning] = useState(false)
  const [loading, setLoading] = useState(true)
  const [checking, setChecking] = useState(false)

  const checkStatus = async () => {
    if (!window.hermesDesktop?.acouz) return
    setChecking(true)
    try {
      const res = await window.hermesDesktop.acouz.isRunning()
      setIsRunning(res.running)
    } catch (err) {
      console.error('Failed to check AcouZ status:', err)
    } finally {
      setChecking(false)
      setLoading(false)
    }
  }

  useEffect(() => {
    checkStatus()
    // Poll every 3 seconds while settings is open to reflect background process state
    const interval = setInterval(checkStatus, 3000)
    return () => clearInterval(interval)
  }, [])

  const handleOpen = async () => {
    if (!window.hermesDesktop?.acouz) return
    triggerHaptic('open')
    try {
      await window.hermesDesktop.acouz.open()
      // Immediately re-check status
      setTimeout(checkStatus, 500)
    } catch (err) {
      console.error('Failed to open AcouZ:', err)
    }
  }

  if (!window.hermesDesktop?.acouz) {
    return null
  }

  return (
    <div className="w-full">
      <h3 className="text-sm font-semibold mb-3 flex items-center gap-2 text-foreground">
        <Mic className="size-4 text-indigo-500" />
        <span>AcouZ (Voiceless Voice Assistant)</span>
      </h3>
      <div className="rounded-lg bg-(--ui-bg-secondary) p-4 border border-(--ui-stroke-secondary)">
        <ListRow
          action={
            <div className="flex items-center gap-3">
              {loading ? (
                <Loader2 className="animate-spin size-4 text-muted-foreground" />
              ) : (
                <div className="flex items-center gap-2">
                  <span className={`size-2 rounded-full ${isRunning ? 'bg-emerald-500 animate-pulse' : 'bg-zinc-400'}`} />
                  <span className="text-xs text-muted-foreground mr-2">
                    {isRunning ? 'Running' : 'Stopped'}
                  </span>
                </div>
              )}
              <Button
                size="sm"
                onClick={handleOpen}
                disabled={checking}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium shadow-xs"
              >
                Open Interface
              </Button>
            </div>
          }
          description="Open the dedicated native interface to configure audio devices, wake words, keyboard hotkeys, and API keys."
          title="AcouZ Control Center"
          wide={false}
        />
      </div>
    </div>
  )
}
