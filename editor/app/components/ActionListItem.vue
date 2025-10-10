<script setup lang="ts">
import type { CustomAction } from '@/types/flow'

defineProps<{
  action: CustomAction
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
            name="i-heroicons-cog-6-tooth"
            class="h-5 w-5 text-purple-600"
          />
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h5 class="text-sm font-semibold text-gray-900 truncate">
              {{ action.name || `Action ${index + 1}` }}
            </h5>
            <UBadge
              :color="action.method === 'GET' ? 'success' : action.method === 'POST' ? 'primary' : action.method === 'PUT' ? 'warning' : action.method === 'DELETE' ? 'error' : 'neutral'"
              variant="subtle"
              size="sm"
            >
              {{ action.method }}
            </UBadge>
          </div>
          <p class="text-xs font-mono text-gray-500 truncate mb-2">
            {{ action.id }}
          </p>
          <p
            v-if="action.description"
            class="text-xs text-gray-600 line-clamp-2"
          >
            {{ action.description }}
          </p>
          <div class="mt-2 flex items-center gap-2 text-xs text-gray-500">
            <UIcon
              name="i-heroicons-globe-alt"
              class="h-3 w-3"
            />
            <span class="truncate">{{ action.url || 'No URL configured' }}</span>
          </div>
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
          <span class="sr-only">Edit action</span>
        </UButton>
        <UButton
          size="sm"
          variant="ghost"
          color="error"
          @click.stop="emit('delete')"
        >
          <UIcon name="i-heroicons-trash" />
          <span class="sr-only">Remove action</span>
        </UButton>
      </div>
    </div>
  </div>
</template>
