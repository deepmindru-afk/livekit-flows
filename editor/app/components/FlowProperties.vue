<script setup lang="ts">
import { computed, ref } from 'vue'
import { useFlows } from '@/composables/useFlows'
import type { CustomAction } from '@/types/flow'

const flowsStore = useFlows()

const isEditModalOpen = ref(false)
const editingActionIndex = ref<number | null>(null)

const editingAction = computed(() => {
  if (editingActionIndex.value === null) return null
  return globalActions.value[editingActionIndex.value] || null
})

const flowName = computed({
  get: () => flowsStore.activeFlow.value?.name || '',
  set: (value: string) => {
    if (flowsStore.activeFlow.value) {
      flowsStore.renameFlow(flowsStore.activeFlow.value.id, value)
    }
  },
})

const systemPrompt = computed({
  get: () => flowsStore.activeFlow.value?.system_prompt || '',
  set: (value: string) => {
    flowsStore.updateActiveFlow((flow) => {
      flow.system_prompt = value
    })
  },
})

const initialNode = computed({
  get: () => flowsStore.activeFlow.value?.initial_node || '',
  set: (value: string) => {
    flowsStore.updateActiveFlow((flow) => {
      flow.initial_node = value
    })
  },
})

const availableNodes = computed(() => {
  return flowsStore.activeFlow.value?.nodes.map(node => ({
    label: `${node.name} (${node.id})`,
    value: node.id,
  })) || []
})

const envVars = computed({
  get: () => flowsStore.activeFlow.value?.environment_variables || {},
  set: (value: Record<string, string>) => {
    flowsStore.updateActiveFlow((flow) => {
      flow.environment_variables = value
    })
  },
})

const envVarList = computed({
  get: () => Object.entries(envVars.value).map(([key, value]) => ({ key, value })),
  set: (list: Array<{ key: string, value: string }>) => {
    const newVars: Record<string, string> = {}
    list.forEach((item) => {
      if (item.key.trim()) {
        newVars[item.key] = item.value
      }
    })
    envVars.value = newVars
  },
})

function addEnvVar() {
  const currentKeys = envVarList.value.map(item => item.key)
  let counter = 1
  const newKey = 'VAR'
  while (currentKeys.includes(`${newKey}${counter > 1 ? counter : ''}`)) {
    counter++
  }
  const finalKey = counter > 1 ? `${newKey}${counter}` : newKey
  envVarList.value = [...envVarList.value, { key: finalKey, value: '' }]
}

function removeEnvVar(index: number) {
  envVarList.value = envVarList.value.filter((_, i) => i !== index)
}

const globalActions = computed({
  get: () => flowsStore.activeFlow.value?.actions || [],
  set: (value: CustomAction[]) => {
    flowsStore.updateActiveFlow((flow) => {
      flow.actions = value
    })
  },
})

function addGlobalAction() {
  const newAction: CustomAction = {
    id: '',
    name: '',
    description: '',
    method: 'GET' as const,
    url: '',
    headers: {},
    timeout: 30,
  }
  globalActions.value = [...globalActions.value, newAction]
}

function removeGlobalAction(index: number) {
  const newActions = [...globalActions.value]
  newActions.splice(index, 1)
  globalActions.value = newActions
}

function openEditModal(index: number) {
  editingActionIndex.value = index
  isEditModalOpen.value = true
}

function updateAction(updatedAction: CustomAction) {
  if (editingActionIndex.value === null) return
  const newActions = [...globalActions.value]
  newActions[editingActionIndex.value] = updatedAction
  globalActions.value = newActions
}

const usageHint = 'Reference these variables in actions using {{VAR_NAME}} syntax'
</script>

<template>
  <div class="space-y-8">
    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            name="i-heroicons-information-circle"
            class="h-5 w-5 text-blue-600"
          />
          <div>
            <h4 class="text-base font-semibold text-gray-900">
              Basic Information
            </h4>
            <p class="text-sm text-gray-600 mt-1">
              Configure the fundamental properties of your conversation flow
            </p>
          </div>
        </div>
      </template>

      <div class="space-y-6">
        <UFormField
          label="Flow Name"
          description="A descriptive name for your conversation flow"
          required
        >
          <UInput
            v-model="flowName"
            placeholder="Customer Support Flow, Product Inquiry Flow"
            size="lg"
            class="font-medium"
          />
        </UFormField>

        <UFormField
          label="System Prompt"
          description="Instructions that guide the AI assistant's behavior throughout the conversation"
          required
        >
          <UTextarea
            v-model="systemPrompt"
            placeholder="You are a helpful customer service assistant. Always be polite, professional, and provide accurate information..."
            :rows="10"
            size="lg"
            class="font-mono text-sm w-full"
          />
          <div class="text-xs text-gray-500 mt-2">
            💡 Tip: Be specific about the assistant's role, tone, and any special instructions
          </div>
        </UFormField>

        <UFormField
          label="Initial Node"
          description="The starting point of your conversation flow"
          required
        >
          <USelect
            v-model="initialNode"
            :items="availableNodes"
            placeholder="Select which node should start the conversation"
            size="lg"
          />
          <div class="text-xs text-gray-500 mt-2">
            🔄 This is where users will begin their journey through your flow
          </div>
        </UFormField>
      </div>
    </UCard>

    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <UIcon
              name="i-heroicons-variable"
              class="h-5 w-5 text-green-600"
            />
            <div>
              <h4 class="text-base font-semibold text-gray-900">
                Environment Variables
              </h4>
              <p class="text-sm text-gray-600 mt-1">
                Define variables that can be used throughout your flow
              </p>
            </div>
          </div>
          <UButton
            size="sm"
            variant="outline"
            color="primary"
            @click="addEnvVar"
          >
            <UIcon name="i-heroicons-plus" />
            Add Variable
          </UButton>
        </div>
      </template>

      <div
        v-if="Object.keys(envVars).length === 0"
        class="text-center py-8"
      >
        <UIcon
          name="i-heroicons-variable"
          class="mx-auto h-12 w-12 text-gray-300 mb-4"
        />
        <h5 class="text-sm font-medium text-gray-900 mb-2">
          No environment variables
        </h5>
        <p class="text-sm text-gray-500 mb-4">
          Add variables to store reusable values like API keys, URLs, or configuration settings
        </p>
        <UButton
          size="sm"
          variant="outline"
          @click="addEnvVar"
        >
          <UIcon name="i-heroicons-plus" />
          Add Your First Variable
        </UButton>
      </div>

      <div
        v-else
        class="space-y-4"
      >
        <div
          v-for="(item, index) in envVarList"
          :key="index"
          class="group relative bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-gray-300 transition-colors"
        >
          <div class="flex items-start gap-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3">
                <div class="flex-1">
                  <UInput
                    v-model="item.key"
                    placeholder="KEY_NAME"
                    size="sm"
                    class="w-full font-mono text-sm font-medium"
                  />
                </div>
                <div class="text-gray-400 text-sm font-mono px-2">
                  =
                </div>
                <div class="flex-1">
                  <UInput
                    v-model="item.value"
                    placeholder="value"
                    size="sm"
                    class="w-full font-mono text-sm"
                  />
                </div>
              </div>
            </div>
            <UButton
              size="sm"
              variant="ghost"
              color="error"
              class="opacity-0 group-hover:opacity-100 transition-opacity"
              @click="removeEnvVar(index)"
            >
              <UIcon name="i-heroicons-trash" />
              <span class="sr-only">Remove variable</span>
            </UButton>
          </div>
        </div>

        <div class="text-xs text-gray-500 bg-blue-50 p-3 rounded-lg">
          💡 <strong>Usage:</strong> {{ usageHint }}
        </div>
      </div>
    </UCard>

    <UCard class="border-0 shadow-sm bg-white">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <UIcon
              name="i-heroicons-cog-6-tooth"
              class="h-5 w-5 text-purple-600"
            />
            <div>
              <h4 class="text-base font-semibold text-gray-900">
                Global Actions
              </h4>
              <p class="text-sm text-gray-600 mt-1">
                Define reusable actions that can be triggered from anywhere in your flow
              </p>
            </div>
          </div>
          <UButton
            size="sm"
            variant="outline"
            color="primary"
            @click="addGlobalAction"
          >
            <UIcon name="i-heroicons-plus" />
            Add Action
          </UButton>
        </div>
      </template>

      <div
        v-if="globalActions.length === 0"
        class="text-center py-8"
      >
        <UIcon
          name="i-heroicons-cog-6-tooth"
          class="mx-auto h-12 w-12 text-gray-300 mb-4"
        />
        <h5 class="text-sm font-medium text-gray-900 mb-2">
          No global actions
        </h5>
        <p class="text-sm text-gray-500 mb-4">
          Actions allow you to make HTTP requests, process data, and integrate with external services
        </p>
        <UButton
          size="sm"
          variant="outline"
          @click="addGlobalAction"
        >
          <UIcon name="i-heroicons-plus" />
          Create Your First Action
        </UButton>
      </div>

      <div
        v-else
        class="space-y-3"
      >
        <ActionListItem
          v-for="(action, index) in globalActions"
          :key="action.id"
          :action="action"
          :index="index"
          @edit="openEditModal(index)"
          @delete="removeGlobalAction(index)"
        />
      </div>
    </UCard>

    <!-- Action Edit Modal -->
    <ActionEditModal
      v-if="editingAction"
      v-model:open="isEditModalOpen"
      :action="editingAction"
      :index="editingActionIndex!"
      @update:action="updateAction"
    />
  </div>
</template>
