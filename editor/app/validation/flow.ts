import { object, string, array, boolean, optional, record, union, literal, pipe, minLength, number } from 'valibot'

export const FieldType = union([literal('string'), literal('integer'), literal('float'), literal('boolean')])
export const HttpMethod = union([literal('GET'), literal('POST'), literal('PUT'), literal('DELETE'), literal('PATCH')])
export const ActionTriggerType = union([literal('on_enter'), literal('on_exit')])

export const DataFieldSchema = object({
  name: string(),
  type: FieldType,
  description: string(),
  required: optional(boolean()),
})

export const ActionTriggerSchema = object({
  trigger_type: ActionTriggerType,
  action_id: string(),
})

export const CustomActionSchema = object({
  id: string(),
  name: string(),
  description: string(),
  method: HttpMethod,
  url: string(),
  headers: optional(record(string(), string())),
  body_template: optional(string()),
  timeout: optional(number()),
  store_response_as: optional(string()),
})

export const EdgeSchema = object({
  id: string(),
  condition: string(),
  target_node_id: optional(string()),
  collect_data: optional(array(DataFieldSchema)),
  actions: optional(array(ActionTriggerSchema)),
})

export const FlowNodeSchema = object({
  id: string(),
  name: string(),
  instruction: optional(string()),
  static_text: optional(string()),
  is_final: optional(boolean()),
  edges: optional(array(EdgeSchema)),
  actions: optional(array(ActionTriggerSchema)),
})

export const ConversationFlowSchema = object({
  system_prompt: pipe(string(), minLength(0)),
  initial_node: string(),
  nodes: array(FlowNodeSchema),
  actions: optional(array(CustomActionSchema)),
  environment_variables: optional(record(string(), string())),
})

export const NodePositionSchema = object({
  x: number(),
  y: number(),
})

export const FlowRecordSchema = object({
  id: string(),
  name: string(),
  system_prompt: pipe(string(), minLength(0)),
  initial_node: string(),
  nodes: array(FlowNodeSchema),
  actions: optional(array(CustomActionSchema)),
  environment_variables: optional(record(string(), string())),
})
