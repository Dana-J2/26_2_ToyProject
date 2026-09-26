FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_PACKED_ASSETS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
WORKDIR /app
COPY requirements-deploy.txt ./
RUN pip install --no-cache-dir -r requirements-deploy.txt
COPY app ./app
COPY deploy/assets ./deploy/assets
COPY deploy/install_assets.py ./deploy/install_assets.py
COPY web_assets/content_matrix.npz web_assets/recipe_row_mapping.csv web_assets/recommendation_rules.joblib web_assets/taste_menu_candidates_v4.csv web_assets/web_settings.json ./web_assets/
RUN python deploy/install_assets.py && rm -rf deploy/assets web_assets/content_matrix.npz
RUN useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 10000
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1 --limit-concurrency 8"]
