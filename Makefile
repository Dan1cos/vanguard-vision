# Define variables
GUI_PYTHON_FILE := frontend/gui.py
GUI_WINDOW_TITLE := My GUI App

# Define targets
run: $(GUI_PYTHON_FILE)
	@./run_app.sh

up:
	@echo "Starting all services..."
	docker compose up --build
	@echo "All services started"

down:
	@echo "Stopping all services..."
	docker compose down
	@echo "All services stopped"

prune: down
	@echo "Cleaning up Docker resources..."
	docker compose down -v --remove-orphans 2>/dev/null || true
	docker system prune -f
	@echo "Cleanup completed"

clean:
	@rm -f *.pyc
	@rm -rf __pycache__

.PHONY: run clean up down prune