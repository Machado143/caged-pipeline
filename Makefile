.PHONY: install lint test sample dbt-parse dbt-build app compose-up compose-down

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests app scripts

test:
	pytest -q

sample:
	python scripts/materialize_sample.py

dbt-parse:
	cd dbt && dbt parse --profiles-dir .

dbt-build: sample
	cd dbt && dbt build --profiles-dir .

app: sample
	streamlit run app/Home.py

compose-up:
	docker compose up --build

compose-down:
	docker compose down
