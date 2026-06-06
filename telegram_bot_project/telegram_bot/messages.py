from __future__ import annotations

from typing import Any


def format_store_message(store_name: str, description: str, featured_products: list[dict[str, Any]] | None = None) -> str:
    msg = (
        f"\U0001f525 {store_name} \U000026a1\n\n"
        f"{description}\n\n"
        f"\U000026a1 Premium Products\n"
        f"\U000026a1 Instant Delivery\n"
        f"\U000026a1 Secure Payment\n"
        f"\U000026a1 24/7 Support"
    )
    return msg


def format_contact_request() -> str:
    return (
        "\U0001f447 *Please share your contact to continue:*\n\n"
        "Tap the *Share Contact* button below to verify your account.\n"
        "We need your phone number for order verification."
    )


def format_category_menu(categories: list[dict[str, Any]]) -> str:
    msg = "*\U0001f3ae Choose Your Game*\n\nSelect a category to browse products:"
    return msg


def format_product_list(category_name: str, products: list[dict[str, Any]]) -> str:
    if not products:
        return f"*{category_name}*\n\nNo products available in this category yet."
    return f"*{category_name}*\n\nSelect a product to view plans:"


def format_plan_list(product_name: str, plans: list[dict[str, Any]]) -> str:
    msg = f"*{product_name}*\n\n*Available Plans:*\n\n"
    for i, plan in enumerate(plans, 1):
        msg += f"{i}. *{plan['duration_days']} Day* - \u20b9{plan['price_inr']}\n"
    msg += "\nSelect a plan to purchase:"
    return msg


def format_order_details(reference_id: str, product_name: str, plan_duration: int, amount: float) -> str:
    return (
        f"\U0001f4cb *Order Created!*\n\n"
        f"\U0001f4cc *Reference:* `{reference_id}`\n"
        f"\U0001f4e6 *Product:* {product_name}\n"
        f"\U0001f4c5 *Plan:* {plan_duration} Day(s)\n"
        f"\U0001f4b0 *Amount:* \u20b9{amount:.2f}\n\n"
        f"Please complete payment using the options below."
    )


def format_payment_success(product_name: str, plan_duration: int, key: str = "") -> str:
    msg = (
        f"\u2705 *Payment Successful!*\n\n"
        f"\U0001f4e6 *Product:* {product_name}\n"
        f"\U0001f4c5 *Plan:* {plan_duration} Day(s)\n\n"
    )
    if key:
        msg += f"\U0001f511 *Your Key:* `{key}`\n\n"
    msg += "\U0001f61c Thank you for your purchase!"
    return msg


def format_payment_failed() -> str:
    return "\u274c *Payment Failed!*\n\nPlease try again or contact support."


def format_my_orders(orders: list[dict[str, Any]]) -> str:
    if not orders:
        return "\U0001f4ed *No Orders Yet*\n\nYou haven't placed any orders yet."
    msg = "\U0001f4e6 *My Orders*\n\n"
    for order in orders:
        status_icon = "\u2705" if order["status"] == "PAID" else "\u23f3" if order["status"] == "PENDING" else "\u274c"
        msg += (
            f"{status_icon} *{order.get('product_name', 'N/A')}*\n"
            f"   \U0001f4c5 {order.get('plan_duration', 'N/A')} Days | \u20b9{order['amount']}\n"
            f"   \U0001f4c6 {order['created_at'][:10]} | `{order['reference_id'][:8]}...`\n\n"
        )
    return msg


def format_announcement(announcement: dict[str, Any]) -> str:
    msg = f"*\U0001f4e2 {announcement.get('title', 'Announcement')}*\n\n{announcement.get('message', '')}"
    return msg


def format_support_message() -> str:
    return (
        "\U0001f4ac *Support*\n\n"
        "Please describe your issue and we'll get back to you shortly.\n\n"
        "Send your message below:"
    )


def format_ticket_created(ticket_id: int) -> str:
    return f"\u2705 *Ticket Created!*\n\nYour ticket ID: `#{ticket_id}`\n\nWe will get back to you shortly."


def format_invalid_option() -> str:
    return "\u274c Invalid option. Please use the buttons below."
