FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/

FROM base AS test
ENV LLM_PROVIDER=openai
ENV OPENAI_API_KEY=sk-test-fake-key-for-ci
ENV CHROMA_HOST=localhost
ENV CHROMA_PORT=8000
CMD ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]

FROM base AS production
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
