import type { InferOutput } from 'valibot'
import type {
  HttpMethod as HttpMethodSchema,
  ActionTriggerType as ActionTriggerTypeSchema,
  ActionTriggerSchema,
  CustomActionSchema,
  EdgeSchema,
  FlowNodeSchema,
  ConversationFlowSchema,
  NodePositionSchema,
  FlowRecordSchema,
} from '@/validation/flow'

export type HttpMethod = InferOutput<typeof HttpMethodSchema>
export type ActionTriggerType = InferOutput<typeof ActionTriggerTypeSchema>

export type ActionTrigger = InferOutput<typeof ActionTriggerSchema>
export type CustomAction = InferOutput<typeof CustomActionSchema>
export type Edge = InferOutput<typeof EdgeSchema>
export type FlowNode = InferOutput<typeof FlowNodeSchema>
export type ConversationFlow = InferOutput<typeof ConversationFlowSchema>
export type NodePosition = InferOutput<typeof NodePositionSchema>
export type FlowRecord = InferOutput<typeof FlowRecordSchema>

export type NodePositionMap = Record<string, NodePosition>
