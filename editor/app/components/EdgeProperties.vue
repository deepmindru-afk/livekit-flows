<script setup lang="ts">
import { computed, ref } from 'vue'
import { useFlows } from '@/composables/useFlows'
import { useSelection } from '@/composables/useSelection'
import type { DataField } from '@/types/flow'

const flowsStore = useFlows()
const selection = useSelection()

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

const edgeDataFields = computed({
  get: () => selectedEdge.value?.edge.collect_data || [],
  set: (value: DataField[]) => {
    if (!selectedEdge.value) return
    flowsStore.updateActiveFlow((flow) => {
      const sourceNode = flow.nodes.find(n => n.id === selectedEdge.value!.sourceNode.id)
      if (sourceNode) {
        const edge = sourceNode.edges?.find(e => e.id === selectedEdge.value!.edge.id)
        if (edge) edge.collect_data = value.length > 0 ? value : undefined
      }
    })
  },
})

// Modal management
const isEditModalOpen = ref(false)
const editingFieldIndex = ref<number | null>(null)
const editingField = ref<DataField | null>(null)

function addEdgeDataField() {
  if (!selectedEdge.value) return
  const newField: DataField = {
    name: '',
    type: 'string' as const,
    description: '',
    required: false,
  }
  const newFields = [...edgeDataFields.value, newField]
  edgeDataFields.value = newFields

  // Open modal for the newly added field
  editingFieldIndex.value = newFields.length - 1
  editingField.value = { ...newField }
  isEditModalOpen.value = true
}

function editField(index: number) {
  editingFieldIndex.value = index
  editingField.value = { ...edgeDataFields.value[index] } as DataField
  isEditModalOpen.value = true
}

function updateField(updatedField: DataField) {
  if (editingFieldIndex.value === null) return

  const newFields = [...edgeDataFields.value]
  newFields[editingFieldIndex.value] = updatedField
  edgeDataFields.value = newFields

  editingFieldIndex.value = null
  editingField.value = null
}

function removeEdgeDataField(index: number) {
  const newFields = [...edgeDataFields.value]
  newFields.splice(index, 1)
  edgeDataFields.value = newFields
}
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

    <!-- Data Collection -->
    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-clipboard-document-list"
            class="h-5 w-5 text-orange-600"
          />
          <div class="flex-1">
            <h4 class="text-base font-semibold text-gray-900">
              Data Collection
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Define what information to collect from the user before following this edge
            </p>
          </div>
          <UButton
            size="sm"
            variant="outline"
            color="primary"
            @click="addEdgeDataField"
          >
            <UIcon name="i-heroicons-plus" />
            Add Field
          </UButton>
        </div>
      </template>

      <div
        v-if="edgeDataFields.length === 0"
        class="text-center py-8"
      >
        <UIcon
          name="i-heroicons-clipboard-document-list"
          class="mx-auto h-12 w-12 text-gray-300 mb-4"
        />
        <h5 class="text-sm font-medium text-gray-900 mb-2">
          No data fields
        </h5>
        <p class="text-sm text-gray-500 mb-4">
          Add fields to collect user input before proceeding along this path
        </p>
        <UButton
          size="sm"
          variant="outline"
          @click="addEdgeDataField"
        >
          <UIcon name="i-heroicons-plus" />
          Add Your First Field
        </UButton>
      </div>

      <div
        v-else
        class="space-y-3"
      >
        <DataFieldListItem
          v-for="(field, index) in edgeDataFields"
          :key="index"
          :field="field"
          :index="index"
          @edit="editField(index)"
          @delete="removeEdgeDataField(index)"
        />

        <div class="text-xs text-gray-500 bg-orange-50 p-3 rounded-lg">
          📝 <strong>Data Collection:</strong> Fields will be collected in order before the conversation follows this edge. Required fields must be provided.
        </div>
      </div>
    </UCard>

    <!-- Edit Modal -->
    <DataFieldEditModal
      v-if="editingField && editingFieldIndex !== null"
      v-model:open="isEditModalOpen"
      :field="editingField"
      :index="editingFieldIndex"
      @update:field="updateField"
    />
  </div>
</template>
