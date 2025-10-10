<script setup lang="ts">
import type { DataField } from '@/types/flow'

defineProps<{
  field: DataField
  index: number
}>()

const emit = defineEmits<{
  edit: []
  delete: []
}>()
</script>

<template>
  <div
    class="group relative bg-white rounded-lg p-4 border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all cursor-pointer"
    @click="emit('edit')"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="flex items-start gap-3 flex-1 min-w-0">
        <div class="flex-shrink-0 mt-0.5">
          <UIcon
            name="i-heroicons-tag"
            class="h-5 w-5 text-orange-600"
          />
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h5 class="text-sm font-semibold text-gray-900 truncate">
              {{ field.name || `Field ${index + 1}` }}
            </h5>
            <UBadge
              :color="field.type === 'string' ? 'primary' : field.type === 'integer' ? 'success' : field.type === 'float' ? 'warning' : 'info'"
              variant="subtle"
              size="sm"
            >
              {{ field.type }}
            </UBadge>
            <UBadge
              :color="field.required ? 'error' : 'neutral'"
              variant="subtle"
              size="sm"
            >
              {{ field.required ? 'Required' : 'Optional' }}
            </UBadge>
          </div>
          <p
            v-if="field.description"
            class="text-xs text-gray-600 line-clamp-2 mt-1"
          >
            {{ field.description }}
          </p>
          <p
            v-else
            class="text-xs text-gray-400 italic"
          >
            No description provided
          </p>
        </div>
      </div>
      <div class="flex-shrink-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
        <UButton
          size="sm"
          variant="ghost"
          color="neutral"
          @click.stop="emit('edit')"
        >
          <UIcon name="i-heroicons-pencil" />
          <span class="sr-only">Edit field</span>
        </UButton>
        <UButton
          size="sm"
          variant="ghost"
          color="error"
          @click.stop="emit('delete')"
        >
          <UIcon name="i-heroicons-trash" />
          <span class="sr-only">Remove field</span>
        </UButton>
      </div>
    </div>
  </div>
</template>
