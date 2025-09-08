<script setup lang="ts">
import { computed } from 'vue'
import { useFlows } from '@/composables/useFlows'
import { useSelection } from '@/composables/useSelection'
import type { DataField, ActionTrigger } from '@/types/flow'

const flowsStore = useFlows()
const selection = useSelection()

const fieldTypeOptions = [
  { label: 'String', value: 'string' },
  { label: 'Integer', value: 'integer' },
  { label: 'Float', value: 'float' },
  { label: 'Boolean', value: 'boolean' },
]

const triggerTypeOptions = [
  { label: 'On Enter', value: 'on_enter' },
  { label: 'On Exit', value: 'on_exit' },
  { label: 'On Edge', value: 'on_edge' },
]

const selectedEdge = computed(() => {
  if (!selection.selectedEdgeId.value || !flowsStore.activeFlow.value) return null

  for (const node of flowsStore.activeFlow.value.nodes) {
    const edge = node.edges?.find(edge => edge.id === selection.selectedEdgeId.value)
    if (edge) return { edge, sourceNode: node }
  }
  return null
})

const availableActions = computed(() => {
  return flowsStore.activeFlow.value?.actions?.map(action => ({
    label: `${action.name} (${action.id})`,
    value: action.id,
  })) || []
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

function addEdgeDataField() {
  if (!selectedEdge.value) return
  const newField = {
    name: '',
    type: 'string' as const,
    description: '',
    required: false,
  }
  edgeDataFields.value = [...edgeDataFields.value, newField]
}

function removeEdgeDataField(index: number) {
  const newFields = [...edgeDataFields.value]
  newFields.splice(index, 1)
  edgeDataFields.value = newFields
}

const edgeActions = computed({
  get: () => selectedEdge.value?.edge.actions || [],
  set: (value: ActionTrigger[]) => {
    if (!selectedEdge.value) return
    flowsStore.updateActiveFlow((flow) => {
      const sourceNode = flow.nodes.find(n => n.id === selectedEdge.value!.sourceNode.id)
      if (sourceNode) {
        const edge = sourceNode.edges?.find(e => e.id === selectedEdge.value!.edge.id)
        if (edge) edge.actions = value.length > 0 ? value : undefined
      }
    })
  },
})

function addEdgeAction() {
  if (!selectedEdge.value) return
  const newAction = {
    trigger_type: 'on_edge' as const,
    action_id: '',
  }
  edgeActions.value = [...edgeActions.value, newAction]
}

function removeEdgeAction(index: number) {
  const newActions = [...edgeActions.value]
  newActions.splice(index, 1)
  edgeActions.value = newActions
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
        class="space-y-4"
      >
        <UCard
          v-for="(field, index) in edgeDataFields"
          :key="index"
          class="border border-gray-200 shadow-sm"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <UIcon
                  name="i-heroicons-tag"
                  class="h-4 w-4 text-orange-600"
                />
                <span class="text-sm font-medium text-gray-900">
                  {{ field.name || `Field ${index + 1}` }}
                </span>
                <UBadge
                  :color="field.required ? 'error' : 'success'"
                  variant="subtle"
                  size="sm"
                >
                  {{ field.required ? 'Required' : 'Optional' }}
                </UBadge>
              </div>
              <UButton
                size="sm"
                variant="ghost"
                color="error"
                @click="removeEdgeDataField(index)"
              >
                <UIcon name="i-heroicons-trash" />
                <span class="sr-only">Remove field</span>
              </UButton>
            </div>
          </template>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <UFormField
              label="Field Name"
              description="Variable name for the collected data"
              required
            >
              <UInput
                v-model="field.name"
                placeholder="e.g., user_email, phone_number"
                size="sm"
              />
            </UFormField>

            <UFormField
              label="Data Type"
              description="Expected format of the user input"
              required
            >
              <USelect
                v-model="field.type"
                :items="fieldTypeOptions"
                placeholder="Select type"
                size="sm"
              />
            </UFormField>

            <UFormField
              label="Description"
              description="Instructions for the user"
              required
            >
              <UInput
                v-model="field.description"
                placeholder="e.g., Please enter your email address"
                size="sm"
              />
            </UFormField>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-200">
            <USwitch
              v-model="field.required"
              label="Required Field"
              description="User must provide this information to continue"
            />
          </div>
        </UCard>

        <div class="text-xs text-gray-500 bg-orange-50 p-3 rounded-lg">
          📝 <strong>Data Collection:</strong> Fields will be collected in order before the conversation follows this edge. Required fields must be provided.
        </div>
      </div>
    </UCard>

    <!-- Edge Actions -->
    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-play"
            class="h-5 w-5 text-indigo-600"
          />
          <div class="flex-1">
            <h4 class="text-base font-semibold text-gray-900">
              Edge Actions
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Configure actions to trigger when following this edge
            </p>
          </div>
          <UButton
            size="sm"
            variant="outline"
            color="primary"
            @click="addEdgeAction"
          >
            <UIcon name="i-heroicons-plus" />
            Add Action
          </UButton>
        </div>
      </template>

      <div
        v-if="edgeActions.length === 0"
        class="text-center py-8"
      >
        <UIcon
          name="i-heroicons-play"
          class="mx-auto h-12 w-12 text-gray-300 mb-4"
        />
        <h5 class="text-sm font-medium text-gray-900 mb-2">
          No edge actions
        </h5>
        <p class="text-sm text-gray-500 mb-4">
          Actions can be triggered when the conversation follows this edge
        </p>
        <UButton
          size="sm"
          variant="outline"
          @click="addEdgeAction"
        >
          <UIcon name="i-heroicons-plus" />
          Add Your First Action
        </UButton>
      </div>

      <div
        v-else
        class="space-y-4"
      >
        <div
          v-for="(action, index) in edgeActions"
          :key="index"
          class="group relative bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-gray-300 transition-colors"
        >
          <div class="flex items-start gap-4">
            <div class="flex-1 min-w-0">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <UFormField
                  label="Trigger Point"
                  description="When should this action run?"
                >
                  <USelect
                    v-model="action.trigger_type"
                    :items="triggerTypeOptions"
                    placeholder="Select trigger"
                    size="sm"
                  />
                </UFormField>

                <UFormField
                  label="Action to Run"
                  description="Which global action should be executed"
                >
                  <USelect
                    v-model="action.action_id"
                    :items="availableActions"
                    placeholder="Select action"
                    size="sm"
                  />
                </UFormField>
              </div>

              <div class="mt-3 text-xs text-gray-500 bg-indigo-50 p-2 rounded">
                ➡️ <strong>On Edge:</strong> Runs when the conversation follows this transition path
              </div>
            </div>

            <UButton
              size="sm"
              variant="ghost"
              color="error"
              class="opacity-0 group-hover:opacity-100 transition-opacity"
              @click="removeEdgeAction(index)"
            >
              <UIcon name="i-heroicons-trash" />
              <span class="sr-only">Remove action</span>
            </UButton>
          </div>
        </div>

        <div class="text-xs text-gray-500 bg-indigo-50 p-3 rounded-lg">
          🚀 <strong>Edge Actions:</strong> These actions run when the conversation transitions along this edge, after data collection.
        </div>
      </div>
    </UCard>
  </div>
</template>
