FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY app ./app
COPY dbt ./dbt
COPY scripts ./scripts
COPY tests/fixtures ./tests/fixtures

RUN pip install --no-cache-dir -e .

EXPOSE 8501
CMD ["streamlit", "run", "app/Home.py", "--server.address=0.0.0.0"]
