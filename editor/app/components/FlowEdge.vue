<script setup lang="ts">
import { BaseEdge, EdgeLabelRenderer, getBezierPath, type EdgeProps } from '@vue-flow/core'
import { computed } from 'vue'
import { useFlows } from '@/composables/useFlows'

const props = defineProps<EdgeProps>()
const path = computed(() => getBezierPath(props))
const flows = useFlows()

function deleteEdge() {
  const flow = flows.activeFlow.value
  if (!flow) return

  flow.nodes.forEach((node) => {
    node.edges = node.edges?.filter(edge => edge.id !== props.id) || []
  })

  flows.updateActiveFlow(() => {
    // Trigger reactivity
  })
}
</script>

<template>
  <BaseEdge :path="path[0]" />
  <EdgeLabelRenderer>
    <UContextMenu
      :items="[
        [
          {
            label: 'Delete Edge',
            icon: 'i-heroicons-trash',
            onSelect: deleteEdge,
            color: 'error',
          },
        ],
      ]"
    >
      <div
        :style="{ position: 'absolute', transform: `translate(-50%, -50%) translate(${path[1]}px, ${path[2]}px)`, pointerEvents: 'all' }"
        class="nodrag nopan bg-white border rounded px-2 py-1 text-xs cursor-pointer hover:bg-gray-50"
      >
        {{ props.data?.condition || 'true' }}
      </div>
    </UContextMenu>
  </EdgeLabelRenderer>
</template>
