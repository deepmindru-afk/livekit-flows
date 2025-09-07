import { ref, readonly } from 'vue'

const selectedNodeId = ref<string>()
const selectedEdgeId = ref<string>()

export function useSelection() {
  function selectNode(nodeId: string | undefined) {
    selectedNodeId.value = nodeId
    selectedEdgeId.value = undefined
  }

  function selectEdge(edgeId: string | undefined) {
    selectedEdgeId.value = edgeId
    selectedNodeId.value = undefined
  }

  function clearSelection() {
    selectedNodeId.value = undefined
    selectedEdgeId.value = undefined
  }

  return {
    selectedNodeId: readonly(selectedNodeId),
    selectedEdgeId: readonly(selectedEdgeId),
    selectNode,
    selectEdge,
    clearSelection,
  }
}
