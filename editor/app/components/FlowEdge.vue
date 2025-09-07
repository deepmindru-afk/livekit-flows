<script setup lang="ts">
import { BaseEdge, EdgeLabelRenderer, getBezierPath, type EdgeProps } from '@vue-flow/core'
import { computed } from 'vue'

const props = defineProps<EdgeProps>()
const path = computed(() => getBezierPath(props))
</script>

<template>
  <BaseEdge :path="path[0]" />
  <EdgeLabelRenderer>
    <div
      :style="{ position: 'absolute', transform: `translate(-50%, -50%) translate(${path[1]}px, ${path[2]}px)`, pointerEvents: 'all' }"
      class="nodrag nopan bg-white border rounded px-2 py-1 text-xs"
    >
      {{ props.data?.condition || 'true' }}
    </div>
  </EdgeLabelRenderer>
</template>
