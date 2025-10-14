<template>
  <div class="json-schema-editor">
    <div
      ref="editorContainer"
      class="border rounded-lg overflow-hidden min-h-[400px]"
      :class="validationError ? 'border-red-500' : 'border-gray-300'"
      @keydown.stop
      @keyup.stop
      @keypress.stop
    />

    <div
      v-if="validationError"
      class="mt-2 p-2 text-sm text-red-600 bg-red-50 rounded"
    >
      {{ validationError }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import type { init } from 'modern-monaco'
import { formatJsonSchema, validateJsonSchema } from '@/composables/useSchemaConverter'

type Monaco = Awaited<ReturnType<typeof init>>
type IStandaloneCodeEditor = ReturnType<Monaco['editor']['create']>

const props = defineProps<{
  schema: Record<string, unknown> | null | undefined
}>()

const emit = defineEmits<{
  (e: 'update', schema: Record<string, unknown>): void
}>()

const editorContainer = ref<HTMLDivElement>()
const validationError = ref<string>()

let editor: IStandaloneCodeEditor | null = null
let monaco: Monaco | null = null

onMounted(async () => {
  if (!editorContainer.value)
    return

  const { init } = await import('modern-monaco')

  monaco = await init()

  editor = monaco.editor.create(editorContainer.value, {
    value: formatJsonSchema(props.schema),
    language: 'json',
    theme: 'vs',
    fontSize: 14,
    tabSize: 2,
    folding: false,
    tabCompletion: 'off',
    lineNumbers: 'off',
    wordWrap: 'on',
    formatOnPaste: true,
    formatOnType: true,
    readOnly: false,
    domReadOnly: false,
  })

  editorContainer.value.addEventListener('click', () => {
    editor?.focus()
  })

  editor.onDidChangeModelContent(() => {
    handleInput()
  })
})

onUnmounted(() => {
  editor?.dispose()
})

function handleInput() {
  if (!editor)
    return

  const content = editor.getValue()
  const result = validateJsonSchema(content)

  if (result.valid && result.schema) {
    validationError.value = undefined
    emit('update', result.schema)
  }
  else {
    validationError.value = result.error
  }
}
</script>
