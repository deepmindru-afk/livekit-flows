<script setup lang="ts">
import { computed } from 'vue'
import { useSelection } from '@/composables/useSelection'
import FlowProperties from './FlowProperties.vue'
import NodeProperties from './NodeProperties.vue'
import EdgeProperties from './EdgeProperties.vue'

const selection = useSelection()

const showFlowDetails = computed(() => !selection.selectedNodeId.value && !selection.selectedEdgeId.value)
const showNodeDetails = computed(() => !!selection.selectedNodeId.value && !selection.selectedEdgeId.value)
const showEdgeDetails = computed(() => !!selection.selectedEdgeId.value)
</script>

<template>
  <div class="h-full flex flex-col bg-gray-50">
    <div class="flex-1 overflow-y-auto">
      <template v-if="showFlowDetails">
        <FlowProperties />
      </template>

      <template v-else-if="showNodeDetails">
        <NodeProperties />
      </template>

      <template v-else-if="showEdgeDetails">
        <EdgeProperties />
      </template>

      <template v-else>
        <div class="flex items-center justify-center h-full text-gray-500">
          <div class="text-center">
            <UIcon
              name="i-heroicons-cursor-arrow-rays"
              class="mx-auto h-12 w-12 text-gray-400 mb-4"
            />
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              No Selection
            </h3>
            <p class="text-sm">
              Select a node or edge to view and edit its properties
            </p>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
