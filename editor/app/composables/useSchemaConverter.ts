export function validateJsonSchema(schemaString: string): { valid: boolean, error?: string, schema?: Record<string, unknown> } {
  try {
    const schema = JSON.parse(schemaString)

    if (typeof schema !== 'object' || schema === null) {
      return { valid: false, error: 'Schema must be an object' }
    }

    if (schema.type !== 'object') {
      return { valid: false, error: 'Root schema type must be "object"' }
    }

    if (schema.properties && typeof schema.properties !== 'object') {
      return { valid: false, error: 'Properties must be an object' }
    }

    if (schema.required && !Array.isArray(schema.required)) {
      return { valid: false, error: 'Required must be an array' }
    }

    return { valid: true, schema }
  }
  catch (error) {
    return { valid: false, error: error instanceof Error ? error.message : 'Invalid JSON' }
  }
}

export function formatJsonSchema(schema: Record<string, unknown> | null | undefined): string {
  if (!schema || typeof schema !== 'object') {
    return ''
  }

  try {
    return JSON.stringify(schema, null, 2)
  }
  catch {
    return ''
  }
}

export function isSchemaEmpty(schema: Record<string, unknown> | null | undefined): boolean {
  if (!schema || typeof schema !== 'object') {
    return true
  }

  const properties = schema.properties || {}
  return Object.keys(properties).length === 0
}
