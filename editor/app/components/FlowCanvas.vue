<script setup lang="ts">
import { ref, watch } from 'vue'
import { VueFlow, type Node, type Edge, type Connection } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import FlowNode from './FlowNode.vue'
import FlowEdge from './FlowEdge.vue'
import { useFlows } from '@/composables/useFlows'
import { schemaToCanvas } from '@/composables/useFlowConverters'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

const flows = useFlows()
const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

watch(
  () => flows.activeFlow.value,
  (f) => {
    if (!f) {
      nodes.value = []
      edges.value = []
      return
    }
    const { nodes: n, edges: e } = schemaToCanvas(f, flows.activePositions.value)
    nodes.value = n
    edges.value = e
  },
  { immediate: true },
)

function onConnect(params: Connection) {
  flows.updateActiveFlow((f) => {
    const src = f.nodes.find(n => n.id === params.source)
    if (!src) return
    const id = `e-${params.source}-${params.target}-${Date.now()}`
    src.edges = src.edges || []
    src.edges.push({
      id,
      condition: 'true',
      target_node_id: params.target || undefined,
      collect_data: [],
      actions: [],
    })
  })
}

function onNodeDragStop(event: { node: Node }) {
  const { node } = event
  flows.updatePosition(node.id, { x: node.position.x, y: node.position.y })
}
</script>

<template>
  <VueFlow
    :nodes="nodes"
    :edges="edges"
    class="h-full w-full"
    @connect="onConnect"
    @node-drag-stop="onNodeDragStop"
  >
    <Background
      pattern-color="#f0f0f0"
      :gap="20"
    />
    <Controls />
    <MiniMap />

    <template #node-flowNode="p">
      <FlowNode v-bind="p" />
    </template>

    <template #edge-flowEdge="p">
      <FlowEdge v-bind="p" />
    </template>
  </VueFlow>
</template>
