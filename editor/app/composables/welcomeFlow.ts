import type { ConversationFlow } from '@/types/flow'

export const welcomeFlow = {
  system_prompt: 'You are Mario, a friendly pizza assistant. Keep responses simple!',
  initial_node: 'welcome',
  actions: [
    {
      id: 'place_order',
      name: 'Place Order',
      description: 'Submit pizza order',
      method: 'POST' as const,
      url: 'https://api.pizzapalace.com/orders',
      headers: {
        'Authorization': 'Bearer {{PIZZA_API_TOKEN}}',
        'Content-Type': 'application/json',
      },
      body_template: `{
  "customer_name": "{{customer_name}}",
  "pizza_type": "{{pizza_type}}",
  "size": "{{size | default('medium')}}",
  "toppings": "{{toppings | default('')}}",
  "address": "{{address}}",
  "phone": "{{phone | default('')}}",
  "special_instructions": "{{special_instructions | default('')}}",
  "timestamp": "{{timestamp | default('2024-01-01T12:00:00Z')}}"
}`,
      store_response_as: 'order_result',
    },
    {
      id: 'check_status',
      name: 'Check Status',
      description: 'Check order status',
      method: 'GET' as const,
      url: 'https://api.pizzapalace.com/orders/{{order_id}}',
      headers: {
        Authorization: 'Bearer {{PIZZA_API_TOKEN}}',
        Accept: 'application/json',
      },
      store_response_as: 'status_data',
    },
  ],
  nodes: [
    {
      id: 'welcome',
      name: 'Welcome',
      static_text: `🍕 Welcome to Pizza Palace!

What would you like to do?

• Order a pizza
• Check order status`,
      is_final: false,
      edges: [
        {
          id: 'order',
          condition: 'Order pizza',
          target_node_id: 'get_details',
        },
        {
          id: 'check',
          condition: 'Check status',
          target_node_id: 'ask_order_id',
        },
      ],
    },
    {
      id: 'get_details',
      name: 'Order Details',
      instruction: 'Collect pizza order details including customer name, pizza type, size, toppings, and delivery address.',
      is_final: false,
      edges: [
        {
          id: 'details_ready',
          condition: 'All order details collected',
          target_node_id: 'submit_order',
          collect_data: [
            {
              name: 'customer_name',
              type: 'string' as const,
              description: 'Customer full name for the order',
              required: true,
            },
            {
              name: 'pizza_type',
              type: 'string' as const,
              description: 'Type of pizza (e.g., margherita, pepperoni, vegetarian)',
              required: true,
            },
            {
              name: 'size',
              type: 'string' as const,
              description: 'Pizza size (small, medium, large)',
              required: false,
            },
            {
              name: 'toppings',
              type: 'string' as const,
              description: 'Additional toppings (comma-separated list)',
              required: false,
            },
            {
              name: 'address',
              type: 'string' as const,
              description: 'Delivery address',
              required: true,
            },
            {
              name: 'phone',
              type: 'string' as const,
              description: 'Customer phone number for delivery confirmation',
              required: false,
            },
            {
              name: 'special_instructions',
              type: 'string' as const,
              description: 'Any special delivery or preparation instructions',
              required: false,
            },
          ],
        },
      ],
    },
    {
      id: 'submit_order',
      name: 'Submit Order',
      static_text: `{% if order_result and order_result.order_id %}
🎉 Order placed successfully!

**Order #{{ order_result.order_id }}**

**Order Details:**
• Customer: {{ customer_name }}
• Pizza: {{ pizza_type }}{% if size %} ({{ size }}){% endif %}
{% if toppings %}• Toppings: {{ toppings }}{% endif %}
• Address: {{ address }}
{% if phone %}• Phone: {{ phone }}{% endif %}

{% if order_result.estimated_delivery %}
Estimated delivery: {{ order_result.estimated_delivery }}
{% endif %}

{% if order_result.total %}
Total: $ {{ order_result.total }}
{% endif %}

Thank you for choosing Pizza Palace! 🍕
{% else %}
❌ Sorry, we couldn't place your order.

{% if order_result and order_result.error %}
{{ order_result.error }}
{% else %}
Please try again or call us at (555) 123-PIZZA
{% endif %}
{% endif %}`,
      is_final: true,
      edges: [],
      actions: [
        {
          trigger_type: 'on_enter',
          action_id: 'place_order',
        },
      ],
    },
    {
      id: 'ask_order_id',
      name: 'Order Number',
      instruction: 'Ask for the order number to check status.',
      is_final: false,
      edges: [
        {
          id: 'has_id',
          condition: 'Order number provided',
          target_node_id: 'get_status',
          collect_data: [
            {
              name: 'order_id',
              type: 'string' as const,
              description: 'Order number to check status',
              required: true,
            },
          ],
        },
      ],
    },
    {
      id: 'get_status',
      name: 'Check Status',
      static_text: `{% if status_data and status_data.status %}
🍕 Order Status: **{{ status_data.status }}**

**Order #{{ order_id }}**

{% if status_data.estimated_time %}
Estimated delivery: {{ status_data.estimated_time }}
{% endif %}

{% if status_data.message %}
{{ status_data.message }}
{% endif %}
{% else %}
❌ Order #{{ order_id }} not found. Please check your order number and try again.
{% endif %}`,
      is_final: true,
      edges: [],
      actions: [
        {
          trigger_type: 'on_enter',
          action_id: 'check_status',
        },
      ],
    },
  ],
  environment_variables: {
    PIZZA_API_TOKEN: 'secret-api-token',
  },
} satisfies ConversationFlow

export const welcomeFlowPositions = {
  welcome: { x: 320, y: 60 },
  get_details: { x: 480, y: 360 },
  submit_order: { x: 480, y: 580 },
  ask_order_id: { x: 150, y: 370 },
  get_status: { x: 150, y: 580 },
}
