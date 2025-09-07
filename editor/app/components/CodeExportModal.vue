<template>
  <UModal
    v-model:open="isOpen"
    :ui="{
      content: 'w-full max-w-5xl max-h-[90vh] sm:max-w-5xl',
      body: 'sm:p-0 p-0 m-0',
      header: 'px-6 py-4',
      footer: 'px-6 py-4',
    }"
  >
    <template #header>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ format.toUpperCase() }} Export
      </h3>
    </template>

    <template #body>
      <pre class="bg-gray-700 text-gray-100 p-4 rounded-none overflow-x-auto text-sm font-mono max-h-96 overflow-y-auto w-full"><code>{{ code }}</code></pre>
    </template>

    <template #footer>
      <div class="flex justify-end gap-2">
        <UButton
          variant="soft"
          :disabled="!code"
          :icon="copied ? 'i-heroicons-check' : 'i-heroicons-clipboard'"
          @click="copyToClipboard"
        >
          {{ copied ? 'Copied!' : 'Copy to Clipboard' }}
        </UButton>
        <UButton
          variant="outline"
          :disabled="!code"
          icon="i-heroicons-arrow-down-tray"
          @click="downloadFile"
        >
          Download
        </UButton>
      </div>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useFlowExport } from '@/composables/useFlowExport'

interface Props {
  modelValue: boolean
  code: string
  format: string
  filename: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const isOpen = ref(false)
const copied = ref(false)
const flowExportStore = useFlowExport()

// Use computed property to avoid mutating prop
const code = computed(() => props.code)

watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
})

watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
  if (!newValue) {
    copied.value = false
  }
})

const copyToClipboard = async () => {
  const success = await flowExportStore.copyToClipboard(props.code)
  if (success) {
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}

const downloadFile = () => {
  const blob = new Blob([props.code], {
    type: props.format === 'python' ? 'text/plain' : (props.format === 'yaml' ? 'application/x-yaml' : 'application/json'),
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = props.filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>
