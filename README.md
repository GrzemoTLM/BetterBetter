BetterBetter - Sports Betting Performance Tracker
BetterBetter is a modern, full-stack web application designed to help users track, analyze, and visualize their sports betting performance. The platform provides comprehensive tools for responsible gambling management, combining manual data entry with cutting-edge OCR technology.


## Running containers

From the `backend` directory:

```bash
docker compose build
```

```bash
docker compose up -d
```

To stop containers and free ports:

```bash
docker compose down
```

## Seeding the database

Seed scripts are in `seeds/`. Run them inside the backend container:

```bash
docker compose exec backend python seeds/seed_disciplines.py
```

To seed everything in order (single copy/paste block):

```bash
docker compose exec backend python seeds/seed_disciplines.py

docker compose exec backend python seeds/seed_bet_type_dict.py

docker compose exec backend python seeds/seed_currencies.py

docker compose exec backend python seeds/seed_bookmakers.py

docker compose exec backend python seeds/seed_ticket_categories.py

docker compose exec backend python seeds/seed_barcelona_coupons.py
```

You can also run other seeds from `seeds/` (for example `seed_currencies.py`, `seed_bookmakers.py`, `seed_barcelona_coupons.py`).

## Environment configuration (.env)

Copy `.env.example` to `.env` and fill in your own keys/secrets before starting containers. If values change, rebuild images with `docker compose build`.

## Base URLs

Ports may differ depending on your `docker-compose.yml` and `.env`.

- Backend API: `http://localhost:8000/`
- Django admin: `http://localhost:8000/admin/`
- Frontend: `http://localhost:5173/`
- Swagger/DRF docs `http://localhost:8000/swagger/` or `http://localhost:8000/redoc/`

