# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Also includes a standalone Flask (Python) backend for Advaith Industries.

## Flask App (Primary Backend)

Located in `flask-app/`. This is the main backend that serves the Advaith Industries site.

### Stack
- **Language**: Python 3.11
- **Framework**: Flask + Flask-CORS
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Static HTML files served by Flask

### Routes
| Route | Description |
|-------|-------------|
| `GET /` | Home page |
| `GET /about` | About page |
| `GET /products` | Product catalog |
| `GET /contact` | Contact page |
| `POST /contact` | Handle contact form submission |
| `GET /api/data?table=<name>` | Fetch any allowed table from Supabase |
| `GET /api/products?category=<cat>` | Fetch products (optional category filter) |
| `POST /api/contact` | JSON API endpoint for contact form |
| `GET /api/healthz` | Health check |

### Required Secrets
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase anon/service role key

### Supabase Tables
- `products` — product catalog (id, name, description, category, price, image_url, etc.)
- `contacts` — contact form submissions (id, name, company, email, message, created_at)

### Running
```
cd flask-app && python app.py
```

## Node.js Monorepo (Supporting Packages)

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5 (api-server artifact)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
