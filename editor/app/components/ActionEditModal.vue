<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { CustomAction } from '@/types/flow'

const props = defineProps<{
  action: CustomAction
  index: number
}>()

const emit = defineEmits<{
  'update:action': [action: CustomAction]
  'close': []
}>()

const isOpen = defineModel<boolean>('open', { required: true })

const httpMethodOptions = [
  { label: 'GET', value: 'GET' },
  { label: 'POST', value: 'POST' },
  { label: 'PUT', value: 'PUT' },
  { label: 'DELETE', value: 'DELETE' },
  { label: 'PATCH', value: 'PATCH' },
]

const localAction = ref<CustomAction>({ ...props.action })
watch(() => props.action, (newAction) => {
  localAction.value = { ...newAction }
}, { deep: true })

const headersList = computed({
  get: () => {
    if (!localAction.value.headers) return []
    return Object.entries(localAction.value.headers).map(([key, value]) => ({ key, value }))
  },
  set: (list: Array<{ key: string, value: string }>) => {
    const newHeaders: Record<string, string> = {}
    list.forEach((item) => {
      if (item.key.trim()) {
        newHeaders[item.key] = item.value
      }
    })
    localAction.value.headers = newHeaders
  },
})

function addHeader() {
  const currentKeys = headersList.value.map(item => item.key)
  let counter = 1
  const newKey = 'Header'
  while (currentKeys.includes(`${newKey}${counter > 1 ? counter : ''}`)) {
    counter++
  }
  const finalKey = counter > 1 ? `${newKey}${counter}` : newKey
  headersList.value = [...headersList.value, { key: finalKey, value: '' }]
}

function removeHeader(headerIndex: number) {
  headersList.value = headersList.value.filter((_, i) => i !== headerIndex)
}

function saveAndClose() {
  emit('update:action', { ...localAction.value })
  isOpen.value = false
}

function cancel() {
  // Reset to original
  localAction.value = { ...props.action }
  isOpen.value = false
}

const bodyTemplatePlaceholder = '{"name": "{{USER_NAME}}", "email": "{{USER_EMAIL}}"}'
const urlHint = 'Use {{VARIABLE_NAME}} to reference environment variables'
</script>

<template>
  <UModal
    v-model:open="isOpen"
    :ui="{
      content: 'max-w-4xl',
    }"
  >
    <template #header>
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          Edit Action
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          Configure the details for {{ localAction.name || 'this action' }}
        </p>
      </div>
    </template>

    <template #body>
      <div class="space-y-6">
        <UFormField
          label="Action ID"
          description="Unique identifier for this action"
          required
        >
          <UInput
            v-model="localAction.id"
            placeholder="send_email, create_user"
            size="md"
            class="font-mono text-sm w-full"
          />
        </UFormField>

        <UFormField
          label="Action Name"
          description="A descriptive name for this action"
          required
        >
          <UInput
            v-model="localAction.name"
            placeholder="Send Email, Create User, Fetch Data"
            size="md"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="Description"
          description="Optional description to document what this action does"
        >
          <UTextarea
            v-model="localAction.description"
            placeholder="Describe the purpose and behavior of this action"
            size="md"
            :rows="2"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="HTTP Method"
          description="The HTTP method to use for the request"
          required
        >
          <USelect
            v-model="localAction.method"
            :items="httpMethodOptions"
            placeholder="Select HTTP method"
            size="md"
            class="w-full"
          />
        </UFormField>

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
                v-model="localAction.url"
                placeholder="https://api.example.com/v1/users"
                size="md"
                class="w-full"
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
                  v-model.number="localAction.timeout"
                  type="number"
                  placeholder="30"
                  size="md"
                />
              </UFormField>

              <UFormField
                label="Store Response As"
                description="Variable name to store the API response"
              >
                <UInput
                  v-model="localAction.store_response_as"
                  placeholder="api_response"
                  size="md"
                />
              </UFormField>
            </div>
          </div>
        </div>

        <div v-if="localAction.method === 'POST' || localAction.method === 'PUT' || localAction.method === 'PATCH'">
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
              v-model="localAction.body_template"
              :placeholder="bodyTemplatePlaceholder"
              size="md"
              :rows="4"
              class="font-mono text-sm w-full"
            />
            <div class="text-xs text-gray-500 mt-2">
              📝 Supports JSON and variable interpolation
            </div>
          </UFormField>
        </div>

        <div>
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
              @click="addHeader"
            >
              <UIcon name="i-heroicons-plus" />
              Add Header
            </UButton>
          </div>

          <div
            v-if="headersList.length === 0"
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
              v-for="(header, headerIndex) in headersList"
              :key="headerIndex"
              class="group p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center gap-3">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-3">
                    <div class="flex-1">
                      <UInput
                        v-model="header.key"
                        placeholder="Header-Name"
                        size="sm"
                        class="w-full font-mono text-xs font-medium"
                      />
                    </div>
                    <div class="text-gray-400 text-xs font-mono px-2">
                      :
                    </div>
                    <div class="flex-1">
                      <UInput
                        v-model="header.value"
                        placeholder="header value"
                        size="sm"
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
                  @click="removeHeader(headerIndex)"
                >
                  <UIcon name="i-heroicons-trash" />
                  <span class="sr-only">Remove header</span>
                </UButton>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <div class="flex items-center justify-end gap-3">
        <UButton
          variant="outline"
          color="neutral"
          @click="cancel"
        >
          Cancel
        </UButton>
        <UButton
          variant="solid"
          color="primary"
          @click="saveAndClose"
        >
          Save Changes
        </UButton>
      </div>
    </template>
  </UModal>
</template>
