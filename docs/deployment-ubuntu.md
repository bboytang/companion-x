# Companion X — Ubuntu 24.04 deployment

Production target: Ubuntu 24.04, 2 vCPU / 2 GB RAM.

## DNS

Point the domain's A record to the server public IPv4 address.

Recommended:
- @ -> server IPv4
- www -> server IPv4 (optional)

Do not publish PostgreSQL or Redis ports to the internet.

## Server prerequisites

Install Docker Engine + Compose plugin, then clone this repository.

From the repository root:

    cp deploy/.env.production.example deploy/.env.production
    nano deploy/.env.production

Set a strong PostgreSQL password.

Start:

    docker compose --env-file deploy/.env.production -f deploy/docker-compose.prod.yml up -d --build

Check:

    docker compose --env-file deploy/.env.production -f deploy/docker-compose.prod.yml ps

Caddy will request a TLS certificate automatically once DNS points to the server and ports 80/443 are reachable.

Health:

    curl https://8kraw.cloud/health

## Important

The first production boot initializes the pgvector schema from database/001_memory.sql. The database volume is persistent, so the init script only runs automatically on a fresh database volume.

For future schema changes, use explicit migrations rather than editing the initial init script.
