# Diagnostic Test Booking & Payment API

A robust, production-ready backend API built for simulating diagnostic centre bookings, state-machine driven payments, and secure webhook processing.

## 🚀 Tech Stack
* **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Async Python)
* **Database**: PostgreSQL (via Supabase) with `asyncpg`
* **ORM & Migrations**: SQLAlchemy 2.0 & Alembic
* **Authentication**: JWT (JSON Web Tokens) with Role-Based Access Control (RBAC)
* **Deployment**: Docker Compose (Local) / Vercel Serverless (Production)
* **Testing**: Pytest & Pytest-Asyncio

## 🏗️ Architecture & Maintainability
This project rigorously follows a **Clean, Layered Architecture (MVVM-inspired)**:
- `app/api`: FastAPI routers handling HTTP validation via Pydantic schemas.
- `app/services`: Contains 100% of the business logic, transaction boundaries, and state-machine transitions. 
- `app/models`: SQLAlchemy ORM database definitions.
- `app/core`: Application-wide configurations, central exception handling, and a dedicated `strings.py` module to eliminate hardcoded values.

## 🔒 Edge Cases & Security
* **Idempotency**: Strict row-level database locks (`SELECT ... FOR UPDATE`) are utilized within the Payment services to completely eliminate race conditions and double-spending when webhooks fire simultaneously.
* **Webhook Security**: Cryptographic HMAC SHA256 signature verification ensures that only trusted servers can trigger state changes in the payment pipeline.

## 🐳 Running Locally (Docker)
1. Clone the repository.
2. Duplicate `.env.example` to `.env` and fill in local variable configurations.
3. Run `docker-compose up --build`.
4. Access the API at `http://localhost:8000/docs`.

## 🌐 Production Deployment
The application is pre-configured for **Vercel Serverless Functions** (`vercel.json`). Schema migrations are handled explicitly via Alembic to prevent cold-start race conditions.

```bash
# Run migrations against a production database:
alembic upgrade head
```
