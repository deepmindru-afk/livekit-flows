<script setup lang="ts">
import { Position, Handle, type NodeProps } from '@vue-flow/core'
import { NodeToolbar } from '@vue-flow/node-toolbar'

const props = defineProps<NodeProps>()
</script>

<template>
  <div class="vue-flow__node-default">
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
</template>
