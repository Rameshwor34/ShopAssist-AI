TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the current status and delivery information for an order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-1001."
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_info",
            "description": "Get product details, price, stock and description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The product ID, for example PROD-001."
                    }
                },
                "required": ["product_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_return_eligibility",
            "description": "Check whether a customer's order is eligible for return.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-1003."
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    }
]