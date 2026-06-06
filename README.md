# Telegram Store Bot

A production-ready Telegram Store Bot built with Django 5, Django REST Framework, Razorpay, and python-telegram-bot.

## Features

-   Product Categories & Plans with Admin Management
-   Razorpay Payment Integration (UPI, Cards, Netbanking, Wallets)
-   Auto Key/Code Delivery After Successful Payment
-   QR Code Payments
-   Broadcast System with Celery
-   Support Ticket System
-   Admin Dashboard with Analytics
-   CSV Bulk Key Upload
-   Webhook-based Telegram Bot
-   Docker Deployment

## Tech Stack

-   **Backend:** Django 5, DRF 3.15, Celery 5.5
-   **Database:** SQLite (dev), PostgreSQL (optional for production)
-   **Bot:** python-telegram-bot 22.x
-   **Payments:** Razorpay SDK
-   **Deployment:** Docker, Nginx, Gunicorn

## Quick Start

### 1. Environment Setup

```bash
cp .env.example .env
# Edit .env with your settings
```

### 2. Docker (Recommended)

```bash
docker compose up -d --build
```

### 3. Manual Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 4. Set Telegram Webhook

The bot runs on webhook mode (required for production). Set the webhook URL:

```bash
# Using management command (recommended)
python manage.py set_telegram_webhook --url https://your-domain.com/telegram/webhook/

# Or via API
curl -X POST http://localhost:8000/telegram/set-webhook/ \
  -d "url=https://your-domain.com/telegram/webhook/"

# Delete webhook (for polling during dev)
python manage.py set_telegram_webhook --delete
```

The webhook endpoint at `/telegram/webhook/` receives Telegram updates, verifies them, and dispatches to the appropriate handler.

Broadcasts run synchronously by default. No Celery/Redis needed.

## Project Structure

```
telegram_bot_project/
├── accounts/          # Telegram user management
├── products/          # Categories, Products, Plans, Keys
├── orders/            # Order management
├── payments/          # Razorpay integration
├── telegram_bot/      # Bot handlers, keyboards, messages
├── announcements/     # Announcements & broadcasts
├── support/           # Support tickets
├── dashboard/         # Admin analytics
└── telegram_bot_project/  # Django project settings
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/telegram/webhook/` | Telegram bot webhook |
| POST | `/api/payments/create/` | Create payment order |
| POST | `/api/payments/verify/` | Verify payment signature |
| POST | `/api/payments/webhook/` | Razorpay webhook |
| GET | `/api/products/categories/` | List categories |
| GET | `/api/products/products/` | List products |
| GET | `/api/products/plans/` | List plans |
| POST | `/api/orders/` | Create order |
| POST | `/api/support/tickets/` | Create support ticket |
| GET | `/api/dashboard/stats/` | Admin dashboard stats |

## Admin Panel

Access the Django admin at `/admin/` to manage:

-   Banner, Categories, Products, Plans
-   Product Keys (single + CSV bulk upload)
-   Orders & Payments
-   Announcements & Broadcasts
-   Support Tickets
-   Telegram Users

## Security

-   Razorpay webhook signature verification
-   Payment signature verification (server-side)
-   CSRF protection
-   Rate limiting via DRF throttling
-   Admin-only endpoints for sensitive operations
