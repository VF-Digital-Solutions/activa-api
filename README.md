# HomeTrack API

Backend REST API for HomeTrack, a household asset management platform that allows tracking routines, habits, reservations, benefits, and different aspects of daily life.

## Tech Stack

- **Python** 3.12
- **Django** 6 + Django REST Framework
- **MySQL** 8
- **Celery** + Redis (task queue and broker)
- **JWT Authentication** via djangorestframework-simplejwt
- **Docker** (MySQL + Redis via Portainer/LXC)

## Features

- Multi-user household management with role-based access (Owner, Admin, Member, Guest)
- Hierarchical household structure (Individual → Family → Community)
- Physical asset tracking with maintenance records, usage logs and documents
- Personal habits with streak tracking
- Shared household routines with member assignment
- Reservations and appointments management
- Credit card benefits and loyalty programs tracking
- Household finances with budgets and recurring expenses
- Multi-channel notifications (push, email, SMS)

## Project Structure

```
hometrack-api/
├── apps/
│   ├── core/           # Base models and utilities
│   ├── identity/       # Users and authentication
│   ├── households/     # Households and memberships
│   ├── assets/         # Physical assets and maintenance
│   ├── routines/       # Habits and household routines
│   ├── reservations/   # Reservations and appointments
│   ├── benefits/       # Card benefits and loyalty programs
│   ├── finances/       # Household finances
│   └── notifications/  # Alerts and notifications
├── api/
│   └── v1/             # API router
├── config/
│   ├── settings/       # Environment-based settings
│   ├── celery.py
│   └── urls.py
└── infrastructure/
    ├── storage/
    ├── messaging/
    └── cache/
```

## Requirements

- Python 3.12+
- MySQL 8
- Redis 7
- pyenv (recommended)

## Local Setup

**1. Clone the repository**

```bash
gh repo clone VF-Digital-Solutions/hometrack-api
cd hometrack-api
```

**2. Create virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your database and Redis credentials
```

**5. Run migrations**

```bash
python manage.py migrate
```

**6. Start development server**

```bash
python manage.py runserver 0.0.0.0:8000
```

## Environment Variables

|Variable     |Description         |Default    |
|-------------|--------------------|-----------|
|`SECRET_KEY` |Django secret key   |—          |
|`DEBUG`      |Debug mode          |`False`    |
|`DB_NAME`    |MySQL database name |—          |
|`DB_USER`    |MySQL user          |—          |
|`DB_PASSWORD`|MySQL password      |—          |
|`DB_HOST`    |MySQL host          |`127.0.0.1`|
|`DB_PORT`    |MySQL port          |`3306`     |
|`REDIS_URL`  |Redis connection URL|—          |

## API Endpoints

|Module       |Base URL                |
|-------------|------------------------|
|Auth         |`/api/v1/auth/`         |
|Households   |`/api/v1/households/`   |
|Assets       |`/api/v1/assets/`       |
|Routines     |`/api/v1/routines/`     |
|Reservations |`/api/v1/reservations/` |
|Benefits     |`/api/v1/benefits/`     |
|Finances     |`/api/v1/finances/`     |
|Notifications|`/api/v1/notifications/`|

## Development Progress

See the [project board](https://github.com/orgs/VF-Digital-Solutions/projects/1) for current development status and roadmap.

## License

Private — All rights reserved.