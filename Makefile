unit_tests:
	pytest --cov ./src --cov-report=term-missing --durations=5 ./tests/unit
