import json
from pathlib import Path


PRODUCTS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "mock_data"
    / "products.json"
)


def get_product_info(product_id: str) -> dict:
    """
    Retrieve product information.
    """

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        products = json.load(file)

    product = products.get(product_id)

    if not product:
        return {
            "success": False,
            "error": f"Product {product_id} was not found."
        }

    return {
        "success": True,
        "product": product
    }