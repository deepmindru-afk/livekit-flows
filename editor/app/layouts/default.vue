<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { useFlows } from '@/composables/useFlows'

const open = ref(false)
const flowsStore = useFlows()

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

// Import/Export functions
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
      // Reset file input
      target.value = ''
    }
    catch (error) {
      console.error('Failed to import flow:', error)
      // TODO: Show error notification
    }
  }
}

function handleExportJson() {
  flowsStore.exportActiveFlow('json')
}

function handleExportYaml() {
  flowsStore.exportActiveFlow('yaml')
}

// Initialize with a flow if none exists
if (flowsStore.flows.value.length === 0) {
  flowsStore.createFlow()
}
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      :default-size="20"
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
      :default-size="50"
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
                { label: 'Export JSON', icon: 'i-heroicons-document-arrow-down', onSelect: handleExportJson },
                { label: 'Export YAML', icon: 'i-heroicons-document-arrow-down', onSelect: handleExportYaml },
              ],
            ]"
          >
            <UButton size="sm">
              <UIcon name="i-heroicons-arrow-down-tray" />
              Export
            </UButton>
          </UDropdownMenu>
        </template>
      </UDashboardNavbar>
      <slot />
    </UDashboardPanel>

    <UDashboardPanel
      id="property-editor"
      :default-size="30"
    >
      <template #body>
        Property Editor
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
