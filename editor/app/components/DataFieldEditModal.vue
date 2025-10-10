<script setup lang="ts">
import { ref, watch } from 'vue'
import type { DataField } from '@/types/flow'

const props = defineProps<{
  field: DataField
  index: number
}>()

const emit = defineEmits<{
  'update:field': [field: DataField]
  'close': []
}>()

const isOpen = defineModel<boolean>('open', { required: true })

const fieldTypeOptions = [
  { label: 'String', value: 'string' },
  { label: 'Integer', value: 'integer' },
  { label: 'Float', value: 'float' },
  { label: 'Boolean', value: 'boolean' },
]

const localField = ref<DataField>({ ...props.field })
watch(() => props.field, (newField) => {
  localField.value = { ...newField }
}, { deep: true })

function saveAndClose() {
  emit('update:field', { ...localField.value })
  isOpen.value = false
}

function cancel() {
  // Reset to original
  localField.value = { ...props.field }
  isOpen.value = false
}
</script>

<template>
  <UModal
    v-model:open="isOpen"
    :ui="{
      content: 'max-w-2xl',
    }"
  >
    <template #header>
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          Edit Data Field
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          Configure the details for {{ localField.name || 'this field' }}
        </p>
      </div>
    </template>

    <template #body>
      <div class="space-y-6">
        <UFormField
          label="Field Name"
          description="Variable name for the collected data (e.g., user_email, phone_number)"
          required
        >
          <UInput
            v-model="localField.name"
            placeholder="user_email, phone_number, order_id"
            size="md"
            class="font-mono text-sm w-full"
          />
        </UFormField>

        <UFormField
          label="Data Type"
          description="Expected format of the user input"
          required
        >
          <USelect
            v-model="localField.type"
            :items="fieldTypeOptions"
            placeholder="Select data type"
            size="md"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="Description"
          description="Instructions or prompt shown to the user when collecting this field"
          required
        >
          <UTextarea
            v-model="localField.description"
            placeholder="Please enter your email address"
            size="md"
            :rows="3"
            class="w-full"
          />
          <div class="text-xs text-gray-500 mt-2">
            💡 This text will be shown to the user as a prompt
          </div>
        </UFormField>

        <div class="pt-4 border-t border-gray-200">
          <USwitch
            v-model="localField.required"
            label="Required Field"
            description="User must provide this information to continue"
          />
        </div>

        <div class="bg-orange-50 p-4 rounded-lg">
          <div class="flex items-start gap-3">
            <UIcon
              name="i-heroicons-information-circle"
              class="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5"
            />
            <div class="text-sm text-orange-900">
              <p class="font-medium mb-1">
                Data Collection Flow
              </p>
              <p class="text-xs text-orange-800">
                When a user reaches this edge, they will be prompted to provide this information. Required fields must be completed before the conversation can continue along this path.
              </p>
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
