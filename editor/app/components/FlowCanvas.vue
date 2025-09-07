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

import { useSelection } from '@/composables/useSelection'

const selection = useSelection()

type SelectableNode = Node & { selected?: boolean }

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
  if (!flows.activeFlow.value) return

  flows.updateActiveFlow((f) => {
    const src = f.nodes.find(n => n.id === params.source)
    if (!src) return
    const id = `e-${params.source}-${params.target}-${Date.now()}`
    src.edges = src.edges || []
    src.edges.push({
      id,
      condition: '',
      target_node_id: params.target || undefined,
      collect_data: [],
      actions: [],
    })
  })

  const { edges: updatedEdges } = schemaToCanvas(flows.activeFlow.value, flows.activePositions.value)
  edges.value = updatedEdges
}

function onNodeDragStop(event: { node: Node }) {
  const { node } = event
  flows.updatePosition(node.id, { x: node.position.x, y: node.position.y })
}

function onNodeClick(event: { node: Node }) {
  nodes.value.forEach((node: SelectableNode) => {
    node.selected = node.id === event.node.id
  })
  selection.selectNode(event.node.id)
}

function onEdgeClick(event: { edge: Edge }) {
  nodes.value.forEach((node: SelectableNode) => {
    node.selected = false
  })
  selection.selectEdge(event.edge.id)
}

function onPaneClick() {
  // Clear all selections when clicking on empty canvas
  nodes.value.forEach((node: SelectableNode) => {
    node.selected = false
  })
  selection.clearSelection()
}

function addNewNode() {
  if (!flows.activeFlow.value) return
  flows.addNode({ x: 300, y: 200 })
}

function deleteSelectedNodes() {
  if (!flows.activeFlow.value) return

  const selectedNodes = nodes.value.filter((node: SelectableNode) => node.selected)
  selectedNodes.forEach((node) => {
    flows.deleteNode(node.id)
  })

  const { nodes: updatedNodes, edges: updatedEdges } = schemaToCanvas(flows.activeFlow.value, flows.activePositions.value)
  nodes.value = updatedNodes
  edges.value = updatedEdges
}

function onKeyDown(event: KeyboardEvent) {
  if (event.key === 'Delete' || event.key === 'Backspace') {
    deleteSelectedNodes()
  }
}
</script>

<template>
  <UContextMenu
    :items="[
      [
        {
          label: 'Add Node',
          icon: 'i-heroicons-plus-circle',
          onSelect: addNewNode,
        },
      ],
    ]"
  >
    <VueFlow
      :nodes="nodes"
      :edges="edges"
      class="h-full w-full"
      :select-nodes-on-drag="false"
      :nodes-draggable="true"
      :nodes-connectable="true"
      :elements-selectable="true"
      @connect="onConnect"
      @node-click="onNodeClick"
      @edge-click="onEdgeClick"
      @pane-click="onPaneClick"
      @node-drag-stop="onNodeDragStop"
      @keydown="onKeyDown"
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
  </UContextMenu>
</template>
