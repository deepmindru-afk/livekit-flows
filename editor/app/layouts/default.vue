<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const open = ref(false)
const selected = ref<string>('basic-flow')

const links = computed(() => [[
  {
    label: 'Basic Flow',
    icon: 'i-lucide-file-text',
    active: selected.value === 'basic-flow',
    onSelect: () => {
      selected.value = 'basic-flow'
    },
  },
  {
    label: 'Cat Facts Flow',
    icon: 'i-lucide-file-text',
    active: selected.value === 'cat-facts-flow',
    onSelect: () => {
      selected.value = 'cat-facts-flow'
    },
  },
  {
    label: 'Data Collection Flow',
    icon: 'i-lucide-file-text',
    active: selected.value === 'data-collection-flow',
    onSelect: () => {
      selected.value = 'data-collection-flow'
    },
  },
], [
  {
    label: 'New Flow',
    icon: 'i-lucide-plus',
    onSelect: () => {
      // TODO: create new flow
    },
  },
]] satisfies NavigationMenuItem[][])

const groups = computed(() => [{
  id: 'flows',
  label: 'Flows',
  items: links.value.flat(),
},
])
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
      <UDashboardNavbar title="Livekit Flows Editor" />
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
