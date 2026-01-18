.PHONY: help install dev build up down logs clean crawl init-db

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev-backend:  ## Run backend in development mode
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:  ## Run frontend in development mode
	cd frontend && npm run dev

build:  ## Build Docker images
	docker-compose build

up:  ## Start all services with Docker
	docker-compose up -d

down:  ## Stop all services
	docker-compose down

logs:  ## View logs
	docker-compose logs -f

clean:  ## Clean up Docker volumes
	docker-compose down -v
	docker system prune -f

init-db:  ## Initialize database with sample data
	cd backend && python ../scripts/init_db.py

crawl:  ## Run crawler to fetch articles
	cd backend && python ../scripts/run_crawler.py

test:  ## Run tests
	cd backend && pytest
	cd frontend && npm test
