Django ETL Pipeline: High-Performance Data Migration

This repository contains a production-grade Extract, Transform, Load (ETL) pipeline built with Django and PostgreSQL. The system is designed to migrate 500,000 legacy order records containing nested JSON data into a normalized relational database schema.

The pipeline focuses on advanced Django ORM optimization techniques, specifically utilizing server-side cursors (`iterator()`) for memory safety and batched insertions (`bulk_create()`) for maximum network throughput. It is fully containerized, idempotent, and resumable.

## Architecture & Technologies

- **Framework:** Django 4.2+
- **Database:** PostgreSQL 15
- **Infrastructure:** Docker & Docker Compose
- **Language:** Python 3.11

## Prerequisites

Ensure you have the following installed on your host machine:

- Docker
- Docker Compose

## Infrastructure Setup

The project is entirely containerized. To build the images and spin up the database and application containers, run the following command in the root directory:

```bash
docker-compose up --build -d
```

Verify that the database healthcheck has passed and the application is running:

```bash
docker-compose ps
```

Once the containers are healthy, apply the database schema migrations:

```bash
docker-compose exec app python manage.py migrate
```

## Data Seeding

Before running the migration pipeline, you must populate the database with the baseline legacy data. The included seeder command will generate exactly 500,000 unique records.

Run the seeder:

```bash
docker-compose exec app python manage.py seed_legacy_data
```

## Running the ETL Pipeline

The core logic is encapsulated in a robust management command named migrate_orders. It supports batching, dry-runs, and resumability.

### Basic Execution

To run the full migration with the optimal batch size of 1000:

```bash
docker-compose exec app python manage.py migrate_orders --batch-size 1000
```

### Dry Run Mode

To test the pipeline logic and calculate expected processing volume without committing any changes to the database:

```bash
docker-compose exec app python manage.py migrate_orders --dry-run
```

### Resuming a Migration

If the pipeline fails mid-execution (e.g., due to a server crash), you can resume from a specific external ID to avoid re-evaluating the entire table:

```bash
docker-compose exec app python manage.py migrate_orders --start-from "legacy-1234abcd"
```

## Performance Benchmarking

The system has been rigorously profiled using Python's tracemalloc for memory footprint analysis and Django query logging for network I/O efficiency.

Please refer to the benchmark.md file in this repository for a complete breakdown of execution times, throughput metrics (records per second), and memory optimization proof.
