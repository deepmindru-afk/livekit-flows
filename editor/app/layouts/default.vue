<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { useFlows } from '@/composables/useFlows'
import { useFlowExport } from '@/composables/useFlowExport'
import FlowInspector from '@/components/FlowInspector.vue'
import CodeExportModal from '@/components/CodeExportModal.vue'

const open = ref(false)
const flowsStore = useFlows()
const flowExportStore = useFlowExport()

const exportModalOpen = ref(false)
const exportCode = ref('')
const exportFormat = ref('')
const exportFilename = ref('')

const flowLinks = computed(() => flowsStore.flows.value.map(flow => ({
  label: flow.name,
  icon: 'i-lucide-file-text',
  active: flowsStore.activeFlowId.value === flow.id,
  onSelect: () => flowsStore.selectFlow(flow.id),
})))

const actionLinks = computed(() => [{
  label: 'New Flow',
  icon: 'i-lucide-plus',
  onSelect: () => flowsStore.createFlow(),
}])

const links = computed(() => [flowLinks.value, actionLinks.value] satisfies NavigationMenuItem[][])

const groups = computed(() => [{
  id: 'flows',
  label: 'Flows',
  items: links.value.flat(),
}])

const importFileRef = ref<HTMLInputElement>()
function handleImport() {
  importFileRef.value?.click()
}

async function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    try {
      await flowsStore.importFlowFromFile(file)
      target.value = ''
    }
    catch (error) {
      console.error('Failed to import flow:', error)
      // TODO: Show error notification
    }
  }
}

function handleExportJson() {
  const code = flowExportStore.getFlowContent('json')
  if (code) {
    exportCode.value = code
    exportFormat.value = 'json'
    exportFilename.value = `${flowExportStore.activeFlow.value?.name || 'flow'}.json`
    exportModalOpen.value = true
  }
}

function handleExportYaml() {
  const code = flowExportStore.getFlowContent('yaml')
  if (code) {
    exportCode.value = code
    exportFormat.value = 'yaml'
    exportFilename.value = `${flowExportStore.activeFlow.value?.name || 'flow'}.yaml`
    exportModalOpen.value = true
  }
}

function handleExportWorkerCode() {
  const code = flowExportStore.getWorkerCode()
  if (code) {
    exportCode.value = code
    exportFormat.value = 'python'
    exportFilename.value = `${flowExportStore.activeFlow.value?.name || 'flow'}_worker.py`
    exportModalOpen.value = true
  }
}

function handleAddNode() {
  flowsStore.addNode({ x: 300, y: 200 })
}

if (flowsStore.flows.value.length === 0) {
  flowsStore.createFlow()
}
</script>

<template>
  <div>
    <UDashboardGroup unit="rem">
      <UDashboardSidebar
        id="default"
        v-model:open="open"
        class="bg-elevated/25"
        :ui="{ footer: 'lg:border-t lg:border-default' }"
      >
        <template #default="{ collapsed }">
          <UDashboardSearchButton
            :collapsed="collapsed"
            class="bg-transparent ring-default"
          />

          <UNavigationMenu
            :collapsed="collapsed"
            :items="links[0]"
            orientation="vertical"
            tooltip
            popover
          />

          <UNavigationMenu
            :collapsed="collapsed"
            :items="links[1]"
            orientation="vertical"
            tooltip
            class="mt-auto"
          />
        </template>
      </UDashboardSidebar>

      <UDashboardSearch :groups="groups" />

      <UDashboardPanel
        id="flow-editor"
        class="flex-grow-3"
      >
        <UDashboardNavbar title="Livekit Flows Editor">
          <template #right>
            <UButton
              size="sm"
              variant="soft"
              @click="handleImport"
            >
              <UIcon name="i-heroicons-arrow-up-tray" />
              Import
            </UButton>

            <input
              ref="importFileRef"
              type="file"
              class="hidden"
              accept=".json,.yaml,.yml"
              @change="handleFileChange"
            >

            <UDropdownMenu
              :items="[
                [
                  { label: 'JSON', icon: 'i-heroicons-document-text', onSelect: handleExportJson },
                  { label: 'YAML', icon: 'i-heroicons-document-text', onSelect: handleExportYaml },
                  { label: 'LiveKit Worker', icon: 'i-heroicons-code-bracket', onSelect: handleExportWorkerCode },
                ],
              ]"
            >
              <UButton
                size="sm"
                variant="soft"
              >
                <UIcon name="i-heroicons-arrow-down-tray" />
                Export
              </UButton>
            </UDropdownMenu>

            <UButton
              size="sm"
              title="Add a new node to the flow"
              @click="handleAddNode"
            >
              <UIcon name="i-heroicons-plus-circle" />
              Add Node
            </UButton>
          </template>
        </UDashboardNavbar>

        <slot />
      </UDashboardPanel>

      <UDashboardPanel
        id="property-editor"
        class="flex-grow-2"
      >
        <FlowInspector />
      </UDashboardPanel>
    </UDashboardGroup>

    <CodeExportModal
      v-model="exportModalOpen"
      :code="exportCode"
      :format="exportFormat"
      :filename="exportFilename"
    />
  </div>
</template>
