from backend.tools.orders import get_order_status
from backend.tools.products import get_product_info
from backend.tools.returns import check_return_eligibility


TOOL_REGISTRY = {
    "get_order_status": get_order_status,
    "get_product_info": get_product_info,
    "check_return_eligibility": check_return_eligibility,
}