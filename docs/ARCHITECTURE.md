# Architecture

## Vue d ensemble

* Frontend: React + TypeScript + Vite + Tailwind (UI compatibles shadcn)
* Backend: FastAPI (Python 3.11+), SQLAlchemy, Alembic, Pydantic v2
* DB: a definir (SQLite dev, Postgres prod)
* Auth: JWT
* Observabilite: logs JSON, request_id

## Principes

* Windows-first: scripts .ps1
* Separation nette front/back
* Validation stricte (Pydantic v2)
* Perf Gate p95 < 500 ms (endpoints critiques)

## Conventions

* ASCII uniquement
* Headers securite, rate limit
* Pagination par defaut sur les listes
