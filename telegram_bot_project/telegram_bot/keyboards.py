from __future__ import annotations

from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton("\U0001f6d2 Start Shopping")],
        [KeyboardButton("\U0001f4e2 Latest Updates"), KeyboardButton("\U0001f4ac Support")],
        [KeyboardButton("\U0001f4e6 My Orders")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def contact_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton("\U0001f4f1 Share Contact", request_contact=True)
    return ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def category_keyboard(categories: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(cat["name"], callback_data=f"cat_{cat['id']}")])
    buttons.append([InlineKeyboardButton("\u2190 Back to Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)


def product_keyboard(products: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for prod in products:
        buttons.append([InlineKeyboardButton(prod["name"], callback_data=f"prod_{prod['id']}")])
    buttons.append([InlineKeyboardButton("\u2190 Back to Categories", callback_data="back_categories")])
    return InlineKeyboardMarkup(buttons)


def plan_keyboard(plans: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for plan in plans:
        label = f"{plan['duration_days']} Day(s) - \u20b9{plan['price_inr']}"
        buttons.append([InlineKeyboardButton(label, callback_data=f"plan_{plan['id']}")])
    buttons.append([InlineKeyboardButton("\u2190 Back to Products", callback_data="back_products")])
    return InlineKeyboardMarkup(buttons)


def payment_qr_keyboard(reference_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("\U0001f4cc Check Payment Status", callback_data=f"check_{reference_id}")],
        [InlineKeyboardButton("\u274c Cancel Order", callback_data=f"cancel_{reference_id}")],
    ]
    return InlineKeyboardMarkup(buttons)


def support_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("\U0001f4ac Contact Support", callback_data="new_ticket")],
        [InlineKeyboardButton("\u2190 Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton("\u2190 Back to Main Menu", callback_data="main_menu")]]
    return InlineKeyboardMarkup(buttons)
