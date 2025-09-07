<script setup lang="ts">
import { Position, Handle, type NodeProps } from '@vue-flow/core'
import { NodeToolbar } from '@vue-flow/node-toolbar'
import { useFlows } from '@/composables/useFlows'

const props = defineProps<NodeProps>()
const flows = useFlows()

function deleteNode() {
  flows.deleteNode(props.id)
}
</script>

<template>
  <UContextMenu
    :items="[
      [
        {
          label: 'Delete Node',
          icon: 'i-heroicons-trash',
          onSelect: deleteNode,
          color: 'error',
        },
      ],
    ]"
  >
    <div
      class="vue-flow__node-default"
      :class="{ 'ring-2 ring-blue-500': props.selected }"
    >
      <NodeToolbar :position="Position.Top">
        <span class="text-xs">{{ props.data?.name }}</span>
      </NodeToolbar>
      <div class="p-3">
        <div class="font-semibold text-sm">
          {{ props.data?.name }}
        </div>
        <div
          v-if="props.data?.instruction"
          class="text-xs text-gray-500"
        >
          {{ props.data?.instruction }}
        </div>
        <div
          v-if="props.data?.is_final"
          class="text-xs text-green-600 font-medium"
        >
          Final Node
        </div>
      </div>
      <Handle
        type="target"
        :position="Position.Top"
      />
      <Handle
        type="source"
        :position="Position.Bottom"
      />
    </div>
  </UContextMenu>
</template>
