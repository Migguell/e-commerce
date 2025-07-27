# E-commerce Docker Management Makefile

.PHONY: help build up down restart logs clean test shell status init seed setup

# Default target
help:
	@echo "E-commerce Docker Management Commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start containers in detached mode"
	@echo "  down      - Stop and remove containers"
	@echo "  restart   - Restart all containers"
	@echo "  logs      - View container logs"
	@echo "  clean     - Remove containers, networks, and volumes"
	@echo "  test      - Run tests in API container"
	@echo "  shell     - Access API container shell"
	@echo "  status    - Check container status"
	@echo "  init      - Initialize database migrations"
	@echo "  seed      - Seed database with default data"
	@echo "  setup     - Complete setup (build, up, init, seed)"

# Build Docker images
build:
	@echo "Building Docker images..."
	cp .env.docker .env
	docker-compose build

# Start containers
up:
	@echo "Starting containers..."
	cp .env.docker .env
	docker-compose up -d

# Stop containers
down:
	@echo "Stopping containers..."
	docker-compose down

# Restart containers
restart: down up

# View logs
logs:
	@echo "Viewing container logs..."
	docker-compose logs -f

# Clean up everything
clean:
	@echo "Cleaning up containers, networks, and volumes..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	@echo "Running tests..."
	docker-compose exec api python -m pytest tests/ -v

# Access API container shell
shell:
	@echo "Accessing API container shell..."
	docker-compose exec api /bin/bash

# Check container status
status:
	@echo "Container status:"
	docker-compose ps
	@echo "\nHealth checks:"
	docker-compose exec api curl -f http://localhost:5000/health || echo "API health check failed"

# Initialize database
init:
	@echo "Initializing database..."
	docker-compose exec api flask db init
	docker-compose exec api flask db migrate -m "Initial migration"
	docker-compose exec api flask db upgrade

# Seed database
seed:
	@echo "Seeding database..."
	docker-compose exec api python -c "from app import create_app; from models.order_status import OrderStatus; app = create_app(); app.app_context().push(); OrderStatus.create_default_statuses()"

# Complete setup
setup: build up
	@echo "Waiting for containers to be ready..."
	sleep 15
	@echo "Setup complete! API available at http://localhost:5000"
	@echo "Health check: http://localhost:5000/health"
	@echo "API status: http://localhost:5000/api/status"