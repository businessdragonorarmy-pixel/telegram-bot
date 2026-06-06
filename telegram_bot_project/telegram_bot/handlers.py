from __future__ import annotations

import logging
from typing import Any

from django.conf import settings

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from accounts.models import TelegramUser
from accounts.services import TelegramUserService
from orders.models import Order
from orders.services import OrderService
from payments.services import PaymentService
from products.models import Banner, Category, Plan, Product
from products.services import ProductKeyService
from support.models import SupportTicket

from .keyboards import (
    back_to_main_keyboard,
    category_keyboard,
    contact_keyboard,
    main_menu_keyboard,
    payment_qr_keyboard,
    plan_keyboard,
    product_keyboard,
    remove_keyboard,
    support_keyboard,
)
from .messages import (
    format_category_menu,
    format_contact_request,
    format_invalid_option,
    format_my_orders,
    format_order_details,
    format_payment_failed,
    format_payment_success,
    format_plan_list,
    format_product_list,
    format_support_message,
    format_ticket_created,
    format_store_message,
)
from .services import TelegramBotService

logger = logging.getLogger(__name__)

AWAITING_SUPPORT_MESSAGE = range(1)

bot_service = TelegramBotService()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user:
        return

    TelegramUserService.get_or_create_user(
        telegram_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        language_code=user.language_code or "en",
    )

    banner = Banner.objects.filter(is_active=True).first()
    store_name = getattr(settings, "STORE_NAME", "Premium Store")
    description = getattr(settings, "STORE_DESCRIPTION", "Premium Digital Products")

    message_text = format_store_message(store_name, description)
    keyboard = main_menu_keyboard()

    if banner and banner.image:
        await update.message.reply_photo(
            photo=banner.image.url,
            caption=message_text,
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            message_text,
            reply_markup=keyboard,
            parse_mode="Markdown",
        )


async def shopping_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    try:
        telegram_user = TelegramUser.objects.get(telegram_id=user_id)
    except TelegramUser.DoesNotExist:
        await update.message.reply_text("Please use /start first.")
        return

    if not telegram_user.is_verified:
        await update.message.reply_text(
            format_contact_request(),
            reply_markup=contact_keyboard(),
            parse_mode="Markdown",
        )
        return

    await show_categories(update, context)


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact = update.effective_message.contact
    if not contact:
        return

    user_id = update.effective_user.id
    phone = contact.phone_number or ""

    TelegramUserService.verify_user(telegram_id=user_id, phone_number=phone)

    await update.message.reply_text(
        "\u2705 *Phone Verified!* Welcome to the store.",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    categories = Category.objects.filter(is_active=True).order_by("position")
    cats_data = [{"id": c.id, "name": c.name, "image": c.image.url if c.image else None} for c in categories]

    if not cats_data:
        text = "\u274c No categories available right now."
        if update.callback_query:
            await update.callback_query.edit_message_text(text)
        else:
            await update.message.reply_text(text)
        return

    message_text = format_category_menu(cats_data)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=category_keyboard(cats_data),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            message_text,
            reply_markup=category_keyboard(cats_data),
            parse_mode="Markdown",
        )


async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "back_categories":
        await show_categories(update, context)
        return

    category_id = int(data.replace("cat_", ""))
    try:
        category = Category.objects.get(id=category_id, is_active=True)
    except Category.DoesNotExist:
        await query.edit_message_text("Category not found.")
        return

    products = Product.objects.filter(category=category, is_active=True).order_by("position")
    prods_data = [{"id": p.id, "name": p.name} for p in products]

    message_text = format_product_list(category.name, prods_data)

    if products:
        await query.edit_message_text(
            message_text,
            reply_markup=product_keyboard(prods_data),
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text(message_text)


async def product_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "back_products":
        await show_categories(update, context)
        return

    product_id = int(data.replace("prod_", ""))
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        await query.edit_message_text("Product not found.")
        return

    plans = Plan.objects.filter(product=product, is_active=True).order_by("price_inr")
    plans_data = [{"id": p.id, "duration_days": p.duration_days, "price_inr": float(p.price_inr)} for p in plans]

    if not plans:
        await query.edit_message_text("No plans available for this product.")
        return

    message_text = format_plan_list(product.name, plans_data)
    await query.edit_message_text(
        message_text,
        reply_markup=plan_keyboard(plans_data),
        parse_mode="Markdown",
    )


async def plan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    plan_id = int(query.data.replace("plan_", ""))
    try:
        plan = Plan.objects.get(id=plan_id, is_active=True)
    except Plan.DoesNotExist:
        await query.edit_message_text("Plan not found.")
        return

    user_id = update.effective_user.id
    telegram_user = TelegramUserService.get_user(user_id)
    if not telegram_user:
        await query.edit_message_text("User not found. Please use /start.")
        return

    if plan.stock_enabled:
        available_keys = ProductKeyService.get_available_key_count(plan.product)
        if available_keys == 0:
            await query.edit_message_text("\u274c Sorry, this product is currently out of stock.")
            return

    order = OrderService.create_order(telegram_user, plan.product, plan)
    context.user_data["current_order"] = order.reference_id

    service = PaymentService()
    payment, razorpay_qr, qr_image = service.create_qr_payment(order)

    caption = (
        f"\U0001f4cb *Order Created!*\n\n"
        f"\U0001f4cc *Reference:* `{order.reference_id}`\n"
        f"\U0001f4e6 *Product:* {plan.product.name}\n"
        f"\U0001f4c5 *Plan:* {plan.duration_days} Day(s)\n"
        f"\U0001f4b0 *Amount:* \u20b9{float(order.amount):.2f}\n\n"
        f"\U0001f4f1 *Scan the QR code* with any UPI app to pay.\n"
        f"Auto-delivery after successful payment."
    )

    await query.message.reply_photo(
        photo=qr_image,
        caption=caption,
        reply_markup=payment_qr_keyboard(reference_id=order.reference_id),
        parse_mode="Markdown",
    )
    await query.message.delete()


async def check_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    reference_id = query.data.replace("check_", "")
    order = OrderService.get_order_by_reference(reference_id)

    if not order:
        await query.edit_message_text("Order not found.")
        return

    if order.status == Order.Status.PAID:
        key = order.key_assigned
        msg = format_payment_success(
            product_name=order.product.name,
            plan_duration=order.plan.duration_days,
            key=key or "",
        )
        await query.edit_message_text(msg, parse_mode="Markdown")
    elif order.status == Order.Status.FAILED:
        await query.edit_message_text(format_payment_failed(), parse_mode="Markdown")
    else:
        await query.edit_message_text(
            "\u23f3 Payment is still pending. Please complete the payment.",
            parse_mode="Markdown",
        )


async def my_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    telegram_user = TelegramUserService.get_user(user_id)
    if not telegram_user:
        await update.message.reply_text("Please use /start first.")
        return

    orders = OrderService.get_user_orders(telegram_user)
    orders_data = []
    for o in orders:
        orders_data.append({
            "reference_id": o.reference_id,
            "product_name": o.product.name,
            "plan_duration": o.plan.duration_days,
            "amount": float(o.amount),
            "status": o.status,
            "created_at": o.created_at.isoformat(),
        })

    message_text = format_my_orders(orders_data)
    await update.message.reply_text(
        message_text,
        reply_markup=back_to_main_keyboard(),
        parse_mode="Markdown",
    )


async def announcements_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from announcements.models import Announcement
    announcement = Announcement.objects.filter(is_active=True).order_by("-created_at").first()

    if not announcement:
        await update.message.reply_text("No updates available.")
        return

    msg = f"*\U0001f4e2 {announcement.title}*\n\n{announcement.message}"

    if announcement.image:
        await update.message.reply_photo(
            photo=announcement.image.url,
            caption=msg,
            reply_markup=back_to_main_keyboard(),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            msg,
            reply_markup=back_to_main_keyboard(),
            parse_mode="Markdown",
        )


async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_support_message(),
        reply_markup=support_keyboard(),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def new_ticket_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "\U0001f4ac Please type your message below. We'll get back to you shortly.",
    )
    return AWAITING_SUPPORT_MESSAGE


async def receive_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    message_text = update.message.text

    telegram_user = TelegramUserService.get_user(user_id)
    if not telegram_user:
        await update.message.reply_text("Please use /start first.")
        return ConversationHandler.END

    ticket = SupportTicket.objects.create(
        user=telegram_user,
        message=message_text,
    )

    await update.message.reply_text(
        format_ticket_created(ticket.id),
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def cancel_order_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    reference_id = query.data.replace("cancel_", "")
    order = OrderService.get_order_by_reference(reference_id)

    if not order:
        await query.edit_message_text("Order not found.")
        return

    if order.status == Order.Status.PENDING:
        OrderService.mark_order_failed(order)
        await query.edit_message_text(
            "\u274c Order cancelled successfully.",
            reply_markup=main_menu_keyboard(),
        )
    else:
        await query.edit_message_text(
            "Cannot cancel order that is already processed.",
        )


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    banner = Banner.objects.filter(is_active=True).first()
    store_name = getattr(settings, "STORE_NAME", "Premium Store")

    message_text = format_store_message(store_name, "")

    if banner and banner.image:
        await query.message.reply_photo(
            photo=banner.image.url,
            caption=message_text,
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown",
        )
    else:
        await query.message.reply_text(
            message_text,
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown",
        )

    await query.message.delete()


def get_handlers() -> list:
    return [
        CommandHandler("start", start_command),
        MessageHandler(filters.Text("\U0001f6d2 Start Shopping"), shopping_start),
        MessageHandler(filters.Text("\U0001f4e6 My Orders"), my_orders_handler),
        MessageHandler(filters.Text("\U0001f4e2 Latest Updates"), announcements_handler),
        MessageHandler(filters.Text("\U0001f4ac Support"), support_handler),
        MessageHandler(filters.CONTACT, contact_handler),
        CallbackQueryHandler(category_callback, pattern=r"^cat_|^back_categories$"),
        CallbackQueryHandler(product_callback, pattern=r"^prod_|^back_products$"),
        CallbackQueryHandler(plan_callback, pattern=r"^plan_\d+$"),
        CallbackQueryHandler(check_payment_callback, pattern=r"^check_"),
        CallbackQueryHandler(cancel_order_callback, pattern=r"^cancel_"),
        CallbackQueryHandler(new_ticket_callback, pattern=r"^new_ticket$"),
        CallbackQueryHandler(main_menu_callback, pattern=r"^main_menu$"),
    ]
