# Docker Setup Guide

## Architecture Overview

This project uses a **microservices architecture** with separate containers for each component:

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│                                                              │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐        │
│  │PostgreSQL│◄─┤Dagster       │◄─┤Dagster Daemon │        │
│  │          │  │Webserver     │  │(schedules)    │        │
│  └────▲─────┘  └──────────────┘  └───────────────┘        │
│       │                                                      │
│       │        ┌──────────┐     ┌────────────┐            │
│       └────────┤dbt       │     │Streamlit   │            │
│                │Runner    │     │Dashboard   │            │
│                └──────────┘     └────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.docker .env

# Edit .env with your settings (or use defaults)
nano .env
```

### 2. Build and Start Services

```bash
# Start core services (Postgres, Dagster)
docker-compose up -d

# View logs
docker-compose logs -f dagster-webserver

# Access Dagster UI
open http://localhost:3000
```

### 3. Optional: Start Dashboard

```bash
# Start with dashboard profile
docker-compose --profile dashboard up -d

# Access Streamlit
open http://localhost:8501
```

## Service Details

### PostgreSQL (postgres)
- **Port**: 5432
- **Purpose**: Data warehouse for all analytics data
- **Data**: Persisted in `postgres_data` volume

### Dagster Webserver (dagster-webserver)
- **Port**: 3000
- **Purpose**: UI for orchestrating data pipelines
- **Command**: `dagster dev`

### Dagster Daemon (dagster-daemon)
- **Purpose**: Executes scheduled jobs and sensors
- **Command**: `dagster-daemon run`

### dbt Runner (dbt)
- **Purpose**: Data transformations (on-demand)
- **Usage**: `docker-compose run dbt dbt run`

### Streamlit Dashboard (dashboard)
- **Port**: 8501
- **Purpose**: Analytics dashboard
- **Profile**: `dashboard` (optional)

## Common Commands

### Development
```bash
# Rebuild after code changes
docker-compose build

# Restart specific service
docker-compose restart dagster-webserver

# View logs
docker-compose logs -f [service-name]

# Execute dbt commands
docker-compose run dbt dbt run
docker-compose run dbt dbt test
```

### Debugging
```bash
# Shell into container
docker-compose exec dagster-webserver /bin/bash

# Check service health
docker-compose ps

# Inspect networks
docker network inspect data-platform-example_geopolitical-net
```

### Cleanup
```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Differences from Poetry Setup

### Before (Poetry)
- Single environment with all dependencies
- Manual service management (`./dev_dagster.sh`)
- Local Python environment required
- Tight coupling between services

### After (Docker)
- **Isolated services**: Each component has own container
- **No local Python needed**: Everything runs in containers
- **Reproducible**: Same environment everywhere
- **Industry standard**: Matches production patterns

## Moving Away from Poetry

Poetry is still useful for **local development**, but Docker is better for:
- ✅ **Running the full stack** (all services together)
- ✅ **Production deployments** (Kubernetes, ECS, etc.)
- ✅ **Team consistency** (everyone runs same environment)
- ✅ **CI/CD pipelines** (build once, run anywhere)

Keep `pyproject.toml` for:
- Local development without Docker
- Dependency management
- Testing with pytest

## Multi-Stage Builds

Each Dockerfile uses **multi-stage builds** for optimization:

1. **Builder stage**: Compiles dependencies with build tools
2. **Runtime stage**: Copies only what's needed to run
3. **Result**: Smaller images (~200MB vs 1GB+)

## Environment Variables

Variables are passed from `.env` → `docker-compose.yml` → containers:

```
.env file
   ↓
docker-compose.yml (${VAR:-default})
   ↓
Container environment
```

## Networking

All services communicate via the `geopolitical-net` bridge network:
- Services reference each other by name (e.g., `postgres`, `dagster-webserver`)
- No need for `localhost` or IP addresses
- Isolated from host network (except exposed ports)

## Volumes

### Named Volumes (persistent)
- `postgres_data`: Database files
- `dagster_home`: Dagster metadata

### Bind Mounts (development)
- `./data:/data:ro`: Read-only data files
- Code is **baked into images** (not mounted)

## Health Checks

PostgreSQL has a health check that other services depend on:
```yaml
depends_on:
  postgres:
    condition: service_healthy
```

This ensures Dagster doesn't start before the database is ready.

## Production Considerations

For production, consider:
1. **Secrets management**: Use Docker secrets or vault
2. **Registry**: Push images to Docker Hub/ECR
3. **Orchestration**: Deploy to Kubernetes/ECS
4. **Monitoring**: Add Prometheus/Grafana
5. **Backups**: Automated database backups
6. **Scaling**: Run multiple Dagster workers

## Troubleshooting

### "Connection refused" errors
- Check if postgres is healthy: `docker-compose ps`
- Wait for health check: `docker-compose logs postgres`

### Permission issues
- Ensure `data/` directory exists and is readable
- Check volume mounts: `docker-compose config`

### Out of memory
- Increase Docker memory limit (Docker Desktop settings)
- Reduce chunk sizes in Dagster assets

### Port conflicts
- Check if ports 3000, 5432, 8501 are available
- Change ports in docker-compose.yml if needed

## Next Steps

1. ✅ Services are containerized
2. ⏭️ Test the pipeline: `docker-compose up -d`
3. ⏭️ Materialize assets in Dagster UI
4. ⏭️ Run dbt transformations
5. ⏭️ View results in dashboard
