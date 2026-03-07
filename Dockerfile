# Use lightweight Python image
FROM python:3.11-slim
# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Set working directory
WORKDIR /app
# Copy dependency files
COPY pyproject.toml uv.lock ./
# Install dependencies (without creating a virtual environment inside the container)
RUN uv pip install --system --no-cache -r pyproject.toml
# Copy source code and assets
COPY src/ ./src/
COPY assets/ ./assets/
COPY alembic.ini ./
COPY migrations/ ./migrations/
# Set PYTHONPATH so python sees the nano_banana_bot package
ENV PYTHONPATH=/app/src
# Expose port for Webhook and Metrics
EXPOSE 5000
# Run the bot
CMD ["python", "-m", "nano_banana_bot"]
