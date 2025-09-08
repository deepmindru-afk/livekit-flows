<script setup lang="ts">
import { BaseEdge, EdgeLabelRenderer, getBezierPath, type EdgeProps } from '@vue-flow/core'
import { computed } from 'vue'
import { useFlows } from '@/composables/useFlows'
import { useSelection } from '@/composables/useSelection'

const props = defineProps<EdgeProps>()
const path = computed(() => getBezierPath(props))
const flows = useFlows()
const selection = useSelection()

const isSelected = computed(() => selection.selectedEdgeId.value === props.id)

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

function selectEdge() {
  selection.clearSelection()
  selection.selectEdge(props.id)
}
</script>

<template>
  <BaseEdge
    :path="path[0]"
    :selected="isSelected"
    :style="{
      stroke: isSelected ? '#3B82F6' : '#B1B1B7',
      strokeWidth: isSelected ? '3' : '2',
    }"
  />
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
        :class="[
          'nodrag nopan border rounded px-2 py-1 text-xs cursor-pointer max-w-32 text-center break-words whitespace-pre-wrap',
          isSelected
            ? 'bg-blue-50 border-blue-300 text-blue-800'
            : 'bg-white border-gray-300 hover:bg-gray-50',
        ]"
        @click="selectEdge"
      >
        {{ props.data?.condition || '...' }}
      </div>
    </UContextMenu>
  </EdgeLabelRenderer>
</template>
