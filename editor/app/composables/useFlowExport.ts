import { computed } from 'vue'
import { useFlows } from '@/composables/useFlows'
import { useExport } from '@/composables/useExport'

export function useFlowExport() {
  const flowsStore = useFlows()
  const exportUtil = useExport()

  const activeFlow = computed(() => flowsStore.activeFlow.value)

  const getFlowContent = (format: 'json' | 'yaml') => {
    if (!activeFlow.value) return ''
    return exportUtil.generateFlowContent(activeFlow.value, format)
  }

  const exportActiveFlow = (format: 'json' | 'yaml') => {
    if (!activeFlow.value) return
    const content = getFlowContent(format)
    const filename = `${activeFlow.value.name || 'flow'}.${format}`
    exportUtil.downloadFile(content, filename)
  }

  const getWorkerCode = () => {
    if (!activeFlow.value) return ''
    return exportUtil.generateWorkerCode(activeFlow.value)
  }

  const exportWorkerCode = () => {
    if (!activeFlow.value) return
    const content = getWorkerCode()
    const filename = `${activeFlow.value.name || 'flow'}_worker.py`
    exportUtil.downloadFile(content, filename)
  }

  return {
    activeFlow,
    getFlowContent,
    exportActiveFlow,
    getWorkerCode,
    exportWorkerCode,
    copyToClipboard: exportUtil.copyToClipboard,
  }
}
