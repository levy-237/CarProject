# Car Project

A Django REST API backend for an **electric vehicle (EV) marketplace**. Sellers can publish detailed EV listings; buyers can search, compare, favourite, and chat with sellers. The platform includes AI-powered search assistance and listing comparison via Ollama.

## Features

### Listings
- Create, update, and manage EV car listings with rich metadata (brand, model, trim, battery health, range, heat pump, warranty, Pickerl, etc.)
- Image uploads via **ImageKit**
- Price history tracking
- Listing states: online/offline, premium, sold, reserved, under review
- Advanced filtering (price, mileage, power, battery size, range, charging specs, location, and more)
- Favourites, side-by-side comparison, and recommendations
- Listing reports for moderation

### Users
- Custom user model with JWT authentication (Simple JWT)
- Email verification and password recovery (Mailjet)
- User profiles with location (province, city, zip codes)
- Private and business accounts
- Saved searches

### Cars catalog
- Reference data for brands, models, trims, body types, drivetrains, and conditions
- Trim-level EV specs (battery size, factory range, AC/DC charging)

### Chat
- REST API for chats and messages tied to listings
- Real-time messaging over **WebSockets** (Django Channels + Redis)
- JWT-authenticated WebSocket connections at `ws/chat/<chat_id>/`

### AI
- **AI Advisor** — natural-language search that translates user intent into listing filters
- **AI Comparator** — intelligent comparison of multiple listings
- Powered by **Ollama** (configurable model)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Django 6, Django REST Framework |
| Auth | JWT (`djangorestframework-simplejwt`) |
| Database | PostgreSQL (`psycopg`) |
| Real-time | Django Channels, Daphne, Redis |
| Images | ImageKit |
| Email | Mailjet |
| AI | Ollama |
| Filtering | django-filter |
| CORS | django-cors-headers |

## Prerequisites

- Python 3.11+ (recommended)
- PostgreSQL
- Redis (required for WebSocket chat)
- External service accounts (as needed): ImageKit, Mailjet, Ollama

## Getting Started

### 1. Clone and create a virtual environment

```bash
git clone <repository-url>
cd carproject

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (see [Environment Variables](#environment-variables) below).

### 4. Set up the database

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for Django admin
```

### 5. Run Redis

WebSocket chat requires a running Redis instance on `127.0.0.1:6379` (default in settings).

```bash
redis-server
```

### 6. Start the development server

Use **Daphne** (ASGI) so both HTTP and WebSockets work:

```bash
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

Alternatively, for HTTP-only development:

```bash
python manage.py runserver
```

The API root is available at:

```
http://localhost:8000/api/
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required
DJANGO_SECRET_KEY=your-secret-key

# Database
DB_NAME=carproject
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# ImageKit (listing & profile images)
IMAGEKIT_PUBLIC_KEY=
IMAGEKIT_PRIVATE_KEY=
IMAGEKIT_URL_ENDPOINT=

# Mailjet (email verification & password recovery)
MAILJET_PUBLIC_API_KEY=
MAILJET_SECRET_API_KEY=
MAILJET_SENDER_EMAIL=
MAILJET_SENDER_NAME=

# Ollama (AI advisor & comparator)
OLLAMA_API_KEY=
OLLAMA_HOST=https://ollama.com
AI_MODEL=gpt-oss:120b
```

> **Note:** `DJANGO_SECRET_KEY` is required — the app will not start without it.

## API Overview

Visit `GET /api/` for a discoverable list of all top-level endpoints.

| Area | Base path | Description |
|------|-----------|-------------|
| Listings | `/api/listings/` | CRUD, favourites, compare, reports, images |
| Users | `/api/users/` | Registration, profile, JWT tokens, saved searches |
| Cars | `/api/cars/` | Brands, models, trims, body types, drivetrains, conditions |
| Chat | `/api/chat/` | Chats and messages (REST) |
| AI | `/api/ai/` | AI advisor chat-bot and listing comparator |
| Locations | `/api/province/`, `/api/city/`, `/api/zip/` | Austrian provinces, cities, zip codes |

### Authentication

Most endpoints require a JWT Bearer token.

```bash
# Obtain tokens
POST /api/users/token/
Content-Type: application/json

{"username": "your_username", "password": "your_password"}

# Use the access token
Authorization: Bearer <access_token>

# Refresh
POST /api/users/token/refresh/
{"refresh": "<refresh_token>"}
```

### WebSockets

Connect to a chat room (JWT token passed via query string or headers — see `chat/middleware.py`):

```
ws://localhost:8000/ws/chat/<chat_id>/
```

## Project Structure

```
carproject/
├── config/           # Django settings, URLs, ASGI/WSGI
├── cars/             # Vehicle catalog (brands, models, trims, …)
├── listings/         # Listings, images, filters, price history
├── users/            # Custom user model, auth, saved searches, locations
├── chat/             # REST + WebSocket messaging
├── ai/               # AI advisor and comparator (Ollama)
├── common/           # Shared utilities (email, verification helpers)
├── manage.py
└── requirements.txt
```

## Running Tests

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test listings
python manage.py test users
python manage.py test chat
python manage.py test cars
python manage.py test ai
```

## Django Admin

With a superuser created, access the admin panel at:

```
http://localhost:8000/admin/
```

## Development Notes

- **Debug mode** is enabled by default (`DEBUG = True`). CORS allows all origins in debug mode.
- **Timezone** is set to `Europe/Berlin`.
- **Pagination** defaults to 23 items per page (limit/offset).
- JWT access tokens are configured with a 1-day lifetime for development convenience.
- Listing images are stored as ImageKit URLs; `storage_key` holds the ImageKit file ID.
- New listings start in `is_under_review=True` until approved via the control/management endpoints.

## License

No license file is included yet. Add one if you plan to open-source or share this project.
