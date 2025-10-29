import type { ConversationFlow, FlowNode, Edge as SchemaEdge, NodePositionMap } from '@/types/flow'
import type { Node as VFNode, Edge as VFEdge } from '@vue-flow/core'

export function schemaToCanvas(flow: ConversationFlow, positions?: NodePositionMap): {
  nodes: VFNode[]
  edges: VFEdge[]
  positions: NodePositionMap
} {
  const pos: NodePositionMap = { ...(positions || {}) }
  const nodes: VFNode[] = flow.nodes.map((n, idx) => {
    if (!pos[n.id]) {
      const col = idx % 4
      const row = Math.floor(idx / 4)
      pos[n.id] = { x: 120 + col * 260, y: 80 + row * 180 }
    }
    return { id: n.id, type: 'flowNode', position: pos[n.id]!, data: n, width: 200 }
  })
  const edges: VFEdge[] = []
  for (const node of flow.nodes) {
    for (const e of node.edges || []) {
      edges.push({ id: e.id, type: 'flowEdge', source: node.id, target: e.target_node_id || '', data: e })
    }
  }
  return { nodes, edges, positions: pos }
}

export function canvasToSchema(
  nodes: VFNode[],
  edges: VFEdge[],
  base: Pick<ConversationFlow, 'system_prompt' | 'initial_node' | 'actions' | 'environment_variables'>,
): ConversationFlow {
  const nodeMap: Record<string, FlowNode> = {}
  for (const n of nodes) {
    nodeMap[n.id] = { ...(n.data as FlowNode), id: n.id, edges: [], actions: [] }
  }
  for (const e of edges) {
    const src = e.source
    if (!nodeMap[src]) continue
    const edgeData = e.data as SchemaEdge
    const ed: SchemaEdge = {
      id: edgeData?.id || e.id,
      condition: edgeData?.condition || '',
      target_node_id: e.target,
      input_schema: edgeData?.input_schema,
      actions: edgeData?.actions || [],
    }
    nodeMap[src].edges = nodeMap[src].edges || []
    nodeMap[src].edges!.push(ed)
  }
  return {
    system_prompt: base.system_prompt,
    initial_node: base.initial_node,
    nodes: Object.values(nodeMap),
    actions: base.actions || [],
    environment_variables: base.environment_variables || {},
  }
}
