import json
from pathlib import Path


ORDERS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "mock_data"
    / "orders.json"
)


def get_order_status(order_id: str) -> dict:
    """
    Retrieve the current status of an order.
    """

    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        orders = json.load(file)

    order = orders.get(order_id)

    if not order:
        return {
            "success": False,
            "error": f"Order {order_id} was not found."
        }

    return {
        "success": True,
        "order": order
    }