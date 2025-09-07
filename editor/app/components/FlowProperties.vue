<script setup lang="ts">
import { computed } from 'vue'
import { useFlows } from '@/composables/useFlows'
import type { CustomAction } from '@/types/flow'

const httpMethodOptions = [
  { label: 'GET', value: 'GET' },
  { label: 'POST', value: 'POST' },
  { label: 'PUT', value: 'PUT' },
  { label: 'DELETE', value: 'DELETE' },
  { label: 'PATCH', value: 'PATCH' },
]

const flowsStore = useFlows()

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

const getHeadersList = (actionIndex: number) => {
  return computed({
    get: () => {
      const action = globalActions.value[actionIndex]
      if (!action?.headers) return []
      return Object.entries(action.headers).map(([key, value]) => ({ key, value }))
    },
    set: (list: Array<{ key: string, value: string }>) => {
      const action = globalActions.value[actionIndex]
      if (!action) return

      const newHeaders: Record<string, string> = {}
      list.forEach((item) => {
        if (item.key.trim()) {
          newHeaders[item.key] = item.value
        }
      })
      action.headers = newHeaders
    },
  })
}

function addEnvVar() {
  envVarList.value.push({ key: '', value: '' })
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

const bodyTemplatePlaceholder = '{"name": "{{USER_NAME}}", "email": "{{USER_EMAIL}}"}'
const usageHint = 'Reference these variables in actions using {{ "{{VAR_NAME}}" }} syntax'
const urlHint = 'Use {{ "{{VARIABLE_NAME}}" }} to reference environment variables'

function updateGlobalAction(index: number, field: keyof CustomAction, value: unknown) {
  const newActions = [...globalActions.value]
  const action = newActions[index]
  if (action) {
    (action as Record<keyof CustomAction, unknown>)[field] = value
    globalActions.value = newActions
  }
}
</script>

<template>
  <div class="space-y-8">
    <!-- Basic Info -->
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
            placeholder="e.g., Customer Support Flow, Product Inquiry Flow"
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

    <!-- Environment Variables -->
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
                <div class="flex-shrink-0 w-32">
                  <UInput
                    v-model="item.key"
                    placeholder="KEY_NAME"
                    size="sm"
                    class="font-mono text-sm font-medium"
                  />
                </div>
                <div class="text-gray-400 text-sm font-mono">
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
              @click="envVarList.splice(index, 1)"
            >
              <UIcon name="i-heroicons-trash" />
              <span class="sr-only">Remove variable</span>
            </UButton>
          </div>
        </div>

        <div class="text-xs text-gray-500 bg-blue-50 p-3 rounded-lg">
          💡 <strong>Usage:</strong> {{ usageHint }}
          <br>
          📝 <strong>Format:</strong> <code class="bg-white px-1 py-0.5 rounded text-xs">KEY = value</code>
        </div>
      </div>
    </UCard>

    <!-- Global Actions -->
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
        class="space-y-6"
      >
        <UCard
          v-for="(action, index) in globalActions"
          :key="action.id"
          class="border border-gray-200 shadow-sm"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex items-center gap-2">
                  <UIcon
                    name="i-heroicons-cog-6-tooth"
                    class="h-4 w-4 text-purple-600"
                  />
                  <span class="text-sm font-medium text-gray-900">
                    {{ action.name || `Action ${index + 1}` }}
                  </span>
                  <UBadge
                    :color="action.method === 'GET' ? 'success' : action.method === 'POST' ? 'primary' : action.method === 'PUT' ? 'warning' : action.method === 'DELETE' ? 'error' : 'neutral'"
                    variant="subtle"
                    size="sm"
                  >
                    {{ action.method }}
                  </UBadge>
                </div>
              </div>
              <UButton
                size="sm"
                variant="ghost"
                color="error"
                @click="removeGlobalAction(index)"
              >
                <UIcon name="i-heroicons-trash" />
                <span class="sr-only">Remove action</span>
              </UButton>
            </div>
          </template>

          <div class="space-y-6">
            <!-- Basic Configuration -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <UFormField
                label="Action ID"
                description="Unique identifier for this action"
                required
              >
                <UInput
                  v-model="action.id"
                  placeholder="e.g., send_email, create_user"
                  size="sm"
                  class="font-mono text-sm"
                  @input="updateGlobalAction(index, 'id', $event)"
                />
              </UFormField>

              <UFormField
                label="Action Name"
                description="A descriptive name for this action"
                required
              >
                <UInput
                  v-model="action.name"
                  placeholder="e.g., Send Email, Create User, Fetch Data"
                  size="sm"
                  @input="updateGlobalAction(index, 'name', $event)"
                />
              </UFormField>

              <UFormField
                label="HTTP Method"
                description="The HTTP method to use for the request"
                required
              >
                <USelect
                  v-model="action.method"
                  :items="httpMethodOptions"
                  placeholder="Select HTTP method"
                  size="sm"
                  @update:model-value="updateGlobalAction(index, 'method', $event)"
                />
              </UFormField>
            </div>

            <!-- Request Configuration -->
            <div>
              <h6 class="text-sm font-medium text-gray-900 mb-4 flex items-center gap-2">
                <UIcon
                  name="i-heroicons-globe-alt"
                  class="h-4 w-4 text-gray-600"
                />
                Request Configuration
              </h6>

              <div class="space-y-4">
                <UFormField
                  label="URL"
                  description="The endpoint URL for the HTTP request"
                  required
                >
                  <UInput
                    v-model="action.url"
                    placeholder="https://api.example.com/v1/users"
                    size="sm"
                    @input="updateGlobalAction(index, 'url', $event)"
                  />
                  <div class="text-xs text-gray-500 mt-2">
                    💡 {{ urlHint }}
                  </div>
                </UFormField>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <UFormField
                    label="Timeout (seconds)"
                    description="Maximum time to wait for the response"
                  >
                    <UInput
                      v-model.number="action.timeout"
                      type="number"
                      placeholder="30"
                      size="sm"
                      @input="updateGlobalAction(index, 'timeout', parseInt($event) || 30)"
                    />
                  </UFormField>

                  <UFormField
                    label="Store Response As"
                    description="Variable name to store the API response"
                  >
                    <UInput
                      v-model="action.store_response_as"
                      placeholder="api_response"
                      size="sm"
                      @input="updateGlobalAction(index, 'store_response_as', $event)"
                    />
                  </UFormField>
                </div>
              </div>
            </div>

            <!-- Request Body (conditional) -->
            <div v-if="action.method === 'POST' || action.method === 'PUT' || action.method === 'PATCH'">
              <h6 class="text-sm font-medium text-gray-900 mb-4 flex items-center gap-2">
                <UIcon
                  name="i-heroicons-document-text"
                  class="h-4 w-4 text-gray-600"
                />
                Request Body
              </h6>

              <UFormField
                label="Body Template"
                description="JSON payload or template for the request body"
              >
                <UTextarea
                  v-model="action.body_template"
                  :placeholder="bodyTemplatePlaceholder"
                  size="sm"
                  :rows="4"
                  class="font-mono text-sm w-full"
                  @input="updateGlobalAction(index, 'body_template', $event)"
                />
                <div class="text-xs text-gray-500 mt-2">
                  📝 Supports JSON and variable interpolation
                </div>
              </UFormField>
            </div>

            <!-- Description -->
            <UFormField
              label="Description"
              description="Optional description to document what this action does"
            >
              <UTextarea
                v-model="action.description"
                placeholder="Describe the purpose and behavior of this action"
                size="sm"
                :rows="2"
                class="w-full"
                @input="updateGlobalAction(index, 'description', $event)"
              />
            </UFormField>
          </div>

          <!-- Headers -->
          <div class="mt-6">
            <div class="flex items-center justify-between mb-4">
              <h6 class="text-sm font-medium text-gray-900 flex items-center gap-2">
                <UIcon
                  name="i-heroicons-bars-3"
                  class="h-4 w-4 text-gray-600"
                />
                HTTP Headers
              </h6>
              <UButton
                size="xs"
                variant="outline"
                color="primary"
                @click="getHeadersList(index).value.push({ key: '', value: '' })"
              >
                <UIcon name="i-heroicons-plus" />
                Add Header
              </UButton>
            </div>

            <div
              v-if="!action.headers || Object.keys(action.headers).length === 0"
              class="text-center py-6 bg-gray-50 rounded-lg"
            >
              <UIcon
                name="i-heroicons-bars-3"
                class="mx-auto h-8 w-8 text-gray-300 mb-2"
              />
              <p class="text-sm text-gray-500">
                No headers configured
              </p>
              <p class="text-xs text-gray-400 mt-1">
                Add headers like <code class="bg-white px-1 py-0.5 rounded text-xs">Authorization: Bearer token</code>
              </p>
            </div>

            <div
              v-else
              class="space-y-3"
            >
              <div
                v-for="(header, headerIndex) in getHeadersList(index).value"
                :key="headerIndex"
                class="group p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-3">
                      <div class="flex-shrink-0 w-36">
                        <UInput
                          v-model="header.key"
                          placeholder="Header-Name"
                          size="xs"
                          class="font-mono text-xs font-medium"
                        />
                      </div>
                      <div class="text-gray-400 text-xs font-mono">
                        :
                      </div>
                      <div class="flex-1">
                        <UInput
                          v-model="header.value"
                          placeholder="header value"
                          size="xs"
                          class="w-full font-mono text-xs"
                        />
                      </div>
                    </div>
                  </div>
                  <UButton
                    size="xs"
                    variant="ghost"
                    color="error"
                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                    @click="getHeadersList(index).value.splice(headerIndex, 1)"
                  >
                    <UIcon name="i-heroicons-trash" />
                    <span class="sr-only">Remove header</span>
                  </UButton>
                </div>
              </div>
            </div>
          </div>
        </UCard>
      </div>
    </UCard>
  </div>
</template>
