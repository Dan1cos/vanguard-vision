# Define variables
GUI_PYTHON_FILE := frontend/gui.py
GUI_WINDOW_TITLE := My GUI App

# Define targets
run: $(GUI_PYTHON_FILE)
	@./run_app.sh
clean:
	@rm -f *.pyc
	@rm -rf __pycache__

.PHONY: run clean