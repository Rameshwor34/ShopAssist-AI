from backend.tools.orders import get_order_status


def check_return_eligibility(order_id: str) -> dict:
    """
    Check whether an order is eligible for return.

    Demo policy:
    Delivered orders are eligible for return within 30 days.
    """

    result = get_order_status(order_id)

    if not result["success"]:
        return result

    order = result["order"]

    if order["status"] != "delivered":
        return {
            "success": True,
            "eligible": False,
            "reason": "Only delivered orders can currently be returned."
        }

    return {
        "success": True,
        "eligible": True,
        "reason": "The order is eligible for return under the 30-day return policy."
    }