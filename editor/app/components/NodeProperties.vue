<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useFlows } from '@/composables/useFlows'
import { useSelection } from '@/composables/useSelection'
import type { ActionTrigger } from '@/types/flow'

const flowsStore = useFlows()
const selection = useSelection()

const triggerTypeOptions = [
  { label: 'On Enter', value: 'on_enter' },
  { label: 'On Exit', value: 'on_exit' },
]

const responseModeOptions = [
  { label: 'LLM Instruction', value: 'ai' },
  { label: 'Static Text', value: 'static' },
]

const selectedNode = computed(() => {
  if (!selection.selectedNodeId.value || !flowsStore.activeFlow.value) return null
  return flowsStore.activeFlow.value.nodes.find(node => node.id === selection.selectedNodeId.value) || null
})

const availableActions = computed(() => {
  return flowsStore.activeFlow.value?.actions?.map(action => ({
    label: `${action.name} (${action.id})`,
    value: action.id,
  })) || []
})

const nodeName = computed({
  get: () => selectedNode.value?.name || '',
  set: (value: string) => {
    if (!selectedNode.value) return
    flowsStore.updateActiveFlow((flow) => {
      const node = flow.nodes.find(n => n.id === selectedNode.value!.id)
      if (node) node.name = value
    })
  },
})

const responseMode = ref('ai')

// Watch for changes in selected node to update response mode
watch(selectedNode, (newNode) => {
  if (!newNode) {
    responseMode.value = 'ai'
    return
  }
  responseMode.value = newNode.static_text ? 'static' : 'ai'
}, { immediate: true })

// Watch for changes in response mode to update the node
watch(responseMode, (newMode) => {
  if (!selectedNode.value) return

  flowsStore.updateActiveFlow((flow) => {
    const node = flow.nodes.find(n => n.id === selectedNode.value!.id)
    if (!node) return

    if (newMode === 'static') {
      node.instruction = undefined
    }
    else {
      node.static_text = undefined
    }
  })
})

const nodeInstruction = computed({
  get: () => selectedNode.value?.instruction || '',
  set: (value: string) => {
    if (!selectedNode.value) return
    flowsStore.updateActiveFlow((flow) => {
      const node = flow.nodes.find(n => n.id === selectedNode.value!.id)
      if (node) {
        node.instruction = value || undefined
        if (value) node.static_text = undefined
      }
    })
  },
})

const nodeStaticText = computed({
  get: () => selectedNode.value?.static_text || '',
  set: (value: string) => {
    if (!selectedNode.value) return
    flowsStore.updateActiveFlow((flow) => {
      const node = flow.nodes.find(n => n.id === selectedNode.value!.id)
      if (node) {
        node.static_text = value || undefined
        if (value) node.instruction = undefined
      }
    })
  },
})

const nodeIsFinal = computed({
  get: () => selectedNode.value?.is_final || false,
  set: (value: boolean) => {
    if (!selectedNode.value) return
    flowsStore.updateActiveFlow((flow) => {
      const node = flow.nodes.find(n => n.id === selectedNode.value!.id)
      if (node) node.is_final = value
    })
  },
})

const nodeActions = computed({
  get: () => selectedNode.value?.actions || [],
  set: (value: ActionTrigger[]) => {
    if (!selectedNode.value) return
    flowsStore.updateActiveFlow((flow) => {
      const node = flow.nodes.find(n => n.id === selectedNode.value!.id)
      if (node) node.actions = value.length > 0 ? value : undefined
    })
  },
})

function addNodeAction() {
  if (!selectedNode.value) return
  const newAction = {
    trigger_type: 'on_enter' as const,
    action_id: '',
  }
  nodeActions.value = [...nodeActions.value, newAction]
}

function removeNodeAction(index: number) {
  const newActions = [...nodeActions.value]
  newActions.splice(index, 1)
  nodeActions.value = newActions
}
</script>

<template>
  <div class="space-y-8">
    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-cube"
            class="h-5 w-5 text-green-600"
          />
          <div>
            <h4 class="text-base font-semibold text-gray-900">
              Node Configuration
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Define how this conversation node behaves and interacts with users
            </p>
          </div>
        </div>
      </template>

      <div class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UFormField
            label="Node Name"
            description="A descriptive name for this conversation node"
            required
          >
            <UInput
              v-model="nodeName"
              placeholder="e.g., Greeting, Product Selection"
              size="lg"
              class="font-medium"
            />
          </UFormField>
        </div>

        <UFormField
          label="Response Mode"
          description="Choose how this node should respond to user input"
          required
        >
          <URadioGroup
            v-model="responseMode"
            :items="responseModeOptions"
            orientation="horizontal"
            size="lg"
            class="space-x-6"
          />
        </UFormField>

        <UFormField
          v-if="responseMode === 'ai'"
          label="AI Instructions"
          description="Instructions that guide the AI assistant's response for this node"
          required
        >
          <UTextarea
            v-model="nodeInstruction"
            placeholder="Provide specific instructions for how the AI should respond at this point in the conversation..."
            :rows="8"
            size="lg"
            class="font-mono text-sm w-full"
          />
          <div class="text-xs text-gray-500 mt-2">
            💡 Be specific about the node's purpose, tone, and any special handling needed
          </div>
        </UFormField>

        <UFormField
          v-if="responseMode === 'static'"
          label="Static Response"
          description="Fixed text to display to the user"
          required
        >
          <UTextarea
            v-model="nodeStaticText"
            placeholder="Thank you for your inquiry. A representative will contact you shortly."
            :rows="6"
            size="lg"
            class="w-full"
          />
          <div class="text-xs text-gray-500 mt-2">
            📝 This exact text will be shown to the user instead of an AI-generated response
          </div>
        </UFormField>

        <UFormField
          label="Node Behavior"
          description="Control how this node functions in the conversation flow"
        >
          <div class="space-y-3">
            <USwitch
              v-model="nodeIsFinal"
              label="Final Node"
              description="When enabled, this node ends the conversation after processing"
            />
            <div class="text-xs text-gray-500 bg-amber-50 p-3 rounded-lg">
              ⚠️ <strong>Final nodes:</strong> Mark this node as final if it should terminate the conversation (e.g., goodbye messages, confirmations)
            </div>
          </div>
        </UFormField>
      </div>
    </UCard>

    <!-- Node Actions -->
    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-play"
            class="h-5 w-5 text-blue-600"
          />
          <div class="flex-1">
            <h4 class="text-base font-semibold text-gray-900">
              Node Actions
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Configure actions to trigger at specific points in this node's lifecycle
            </p>
          </div>
          <UButton
            size="sm"
            variant="outline"
            color="primary"
            @click="addNodeAction"
          >
            <UIcon name="i-heroicons-plus" />
            Add Action
          </UButton>
        </div>
      </template>

      <div
        v-if="nodeActions.length === 0"
        class="text-center py-8"
      >
        <UIcon
          name="i-heroicons-play"
          class="mx-auto h-12 w-12 text-gray-300 mb-4"
        />
        <h5 class="text-sm font-medium text-gray-900 mb-2">
          No actions configured
        </h5>
        <p class="text-sm text-gray-500 mb-4">
          Actions can be triggered when entering or exiting this node
        </p>
        <UButton
          size="sm"
          variant="outline"
          @click="addNodeAction"
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
          v-for="(action, index) in nodeActions"
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

              <div class="mt-3 text-xs text-gray-500 bg-blue-50 p-2 rounded">
                <template v-if="action.trigger_type === 'on_enter'">
                  🔄 <strong>On Enter:</strong> Runs when a user first reaches this node
                </template>
                <template v-if="action.trigger_type === 'on_exit'">
                  ↗️ <strong>On Exit:</strong> Runs when a user leaves this node
                </template>
              </div>
            </div>

            <UButton
              size="sm"
              variant="ghost"
              color="error"
              class="opacity-0 group-hover:opacity-100 transition-opacity"
              @click="removeNodeAction(index)"
            >
              <UIcon name="i-heroicons-trash" />
              <span class="sr-only">Remove action</span>
            </UButton>
          </div>
        </div>

        <div class="text-xs text-gray-500 bg-green-50 p-3 rounded-lg">
          💡 <strong>Action Flow:</strong> Actions run in the order they appear above. Use trigger points to control timing.
        </div>
      </div>
    </UCard>
  </div>
</template>
