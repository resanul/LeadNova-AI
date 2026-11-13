.PHONY: help install test test-unit test-integration run-api run-web docker-up docker-down

help:
	@echo "GlobalLead AI - Management Makefile"
	@echo "  make install         Install backend & frontend dependencies"
	@echo "  make test            Run complete Pytest test suite"
	@echo "  make run-api         Start FastAPI backend (Port 8000)"
	@echo "  make run-web         Start Next.js frontend (Port 3000)"
	@echo "  make docker-up       Launch multi-container cloud control plane"
	@echo "  make docker-down     Stop multi-container cloud control plane"

install:
	cd apps/api && pip install -r requirements.txt
	cd apps/admin-web && npm install

test:
	cd apps/api && pytest -v

test-unit:
	cd apps/api && pytest -v tests/test_unit.py

test-integration:
	cd apps/api && pytest -v tests/test_integration.py

run-api:
	cd apps/api && uvicorn app.main:app --reload --port 8000

run-web:
	cd apps/admin-web && npm run dev

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
