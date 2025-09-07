import YAML from 'yaml'
import type { ConversationFlow } from '@/types/flow'
import { workerTemplate } from '@/templates/workerTemplate'

export function useExport() {
  const generateFlowContent = (flow: ConversationFlow, format: 'json' | 'yaml'): string => {
    const payload: ConversationFlow = {
      system_prompt: flow.system_prompt,
      initial_node: flow.initial_node,
      nodes: flow.nodes,
      actions: flow.actions || [],
      environment_variables: flow.environment_variables || {},
    }

    return format === 'yaml' ? YAML.stringify(payload) : JSON.stringify(payload, null, 2)
  }

  const generateWorkerCode = (flow: ConversationFlow): string => {
    const yamlContent = generateFlowContent(flow, 'yaml')
    return workerTemplate.replace('{{YAML_CONTENT}}', yamlContent)
  }

  const downloadFile = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const copyToClipboard = async (content: string): Promise<boolean> => {
    try {
      await navigator.clipboard.writeText(content)
      return true
    }
    catch (err) {
      console.error('Failed to copy to clipboard:', err)
      return false
    }
  }

  return {
    generateFlowContent,
    generateWorkerCode,
    downloadFile,
    copyToClipboard,
  }
}
