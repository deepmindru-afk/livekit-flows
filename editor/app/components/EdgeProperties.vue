<script setup lang="ts">
import { computed } from 'vue'
import { useFlows } from '@/composables/useFlows'
import { useSelection } from '@/composables/useSelection'
import { isSchemaEmpty } from '@/composables/useSchemaConverter'
import JsonSchemaEditor from './JsonSchemaEditor.vue'

const flowsStore = useFlows()
const selection = useSelection()

const schemaKey = computed(() => {
  return `edge-schema-${flowsStore.activeFlowId.value}-${selection.selectedEdgeId.value}`
})

const selectedEdge = computed(() => {
  if (!selection.selectedEdgeId.value || !flowsStore.activeFlow.value) return null

  for (const node of flowsStore.activeFlow.value.nodes) {
    const edge = node.edges?.find(edge => edge.id === selection.selectedEdgeId.value)
    if (edge) return { edge, sourceNode: node }
  }
  return null
})

const edgeCondition = computed({
  get: () => selectedEdge.value?.edge.condition || '',
  set: (value: string) => {
    if (!selectedEdge.value) return
    flowsStore.updateActiveFlow((flow) => {
      const sourceNode = flow.nodes.find(n => n.id === selectedEdge.value!.sourceNode.id)
      if (sourceNode) {
        const edge = sourceNode.edges?.find(e => e.id === selectedEdge.value!.edge.id)
        if (edge) edge.condition = value
      }
    })
  },
})

const inputSchema = computed({
  get: () => selectedEdge.value?.edge.input_schema || null,
  set: (value: Record<string, unknown> | null) => {
    if (!selectedEdge.value) return
    flowsStore.updateActiveFlow((flow) => {
      const sourceNode = flow.nodes.find(n => n.id === selectedEdge.value!.sourceNode.id)
      if (sourceNode) {
        const edge = sourceNode.edges?.find(e => e.id === selectedEdge.value!.edge.id)
        if (edge) {
          edge.input_schema = (value && !isSchemaEmpty(value)) ? value : undefined
        }
      }
    })
  },
})

function updateSchema(schema: Record<string, unknown>) {
  inputSchema.value = schema
}

// Count properties in schema
const propertyCount = computed(() => {
  if (!inputSchema.value) return 0
  const properties = inputSchema.value.properties || {}
  return Object.keys(properties).length
})
</script>

<template>
  <div class="space-y-8">
    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-arrow-right"
            class="h-5 w-5 text-purple-600"
          />
          <div>
            <h4 class="text-base font-semibold text-gray-900">
              Edge Configuration
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Define the transition logic and data collection for this connection
            </p>
          </div>
        </div>
      </template>

      <div class="space-y-6">
        <UFormField
          label="Transition Condition"
          description="Describe the condition or rule that must be true for this edge to be followed"
          required
        >
          <UInput
            v-model="edgeCondition"
            placeholder="e.g. user confirmed order"
            size="lg"
            class="w-full"
          />
        </UFormField>
      </div>
    </UCard>

    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-clipboard-document-list"
            class="h-5 w-5 text-orange-600"
          />
          <div class="flex-1">
            <h4 class="text-base font-semibold text-gray-900">
              Input Schema
              <span
                v-if="propertyCount > 0"
                class="ml-2 text-sm font-normal text-gray-500"
              >
                ({{ propertyCount }} {{ propertyCount === 1 ? 'property' : 'properties' }})
              </span>
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Define data to collect from the user using JSON Schema
            </p>
          </div>
        </div>
      </template>

      <JsonSchemaEditor
        :key="schemaKey"
        :schema="inputSchema"
        @update="updateSchema"
      />

      <div class="mt-4 text-xs text-gray-500 bg-orange-50 p-3 rounded-lg">
        📝 <strong>Input Schema:</strong> Define the structure and validation rules for data collected from users. Uses JSON Schema format for flexible validation.
      </div>
    </UCard>
  </div>
</template>
