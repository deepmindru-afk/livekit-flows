<script setup lang="ts">
import { Position, Handle, type NodeProps } from '@vue-flow/core'
import { useFlows } from '@/composables/useFlows'

const props = defineProps<NodeProps>()
const flows = useFlows()

function deleteNode() {
  flows.deleteNode(props.id)
}
</script>

<template>
  <UContextMenu
    :items="[
      [
        {
          label: 'Delete Node',
          icon: 'i-heroicons-trash',
          onSelect: deleteNode,
          color: 'error',
        },
      ],
    ]"
  >
    <div
      class="bg-white  border border-gray-200 rounded-lg  w-full h-full"
      :class="{ 'ring-2 ring-blue-500 shadow-lg': props.selected }"
    >
      <div class="p-3">
        <div class="font-semibold text-sm text-gray-800 leading-tight">
          {{ props.data?.name }}
        </div>

        <div class="mt-1 min-h-[1.5rem]">
          <div
            v-if="props.data?.instruction && !props.data?.static_text"
            class="text-xs text-gray-700 leading-relaxed overflow-hidden"
            :style="{
              'display': '-webkit-box',
              '-webkit-line-clamp': '3',
              '-webkit-box-orient': 'vertical',
            }"
          >
            {{ props.data.instruction }}
          </div>

          <div
            v-if="props.data?.static_text"
            class="text-xs text-gray-700 leading-relaxed overflow-hidden"
            :style="{
              'display': '-webkit-box',
              '-webkit-line-clamp': '3',
              '-webkit-box-orient': 'vertical',
            }"
          >
            {{ props.data.static_text }}
          </div>

          <div
            v-if="!props.data?.instruction && !props.data?.static_text"
            class="text-xs text-gray-400 italic leading-relaxed"
          >
            No response configured
          </div>
        </div>

        <div class="flex flex-wrap gap-1 mt-1">
          <UBadge
            v-if="props.data?.instruction && !props.data?.static_text"
            color="info"
            variant="subtle"
            size="sm"
          >
            LLM instruction
          </UBadge>

          <UBadge
            v-if="props.data?.static_text"
            color="warning"
            variant="subtle"
            size="sm"
          >
            Static
          </UBadge>

          <UBadge
            v-if="props.data?.is_final"
            color="success"
            variant="subtle"
            size="sm"
          >
            Final
          </UBadge>
        </div>
      </div>
      <Handle
        type="target"
        :position="Position.Top"
      />
      <Handle
        type="source"
        :position="Position.Bottom"
      />
    </div>
  </UContextMenu>
</template>
