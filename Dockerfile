FROM python:3.12-slim
ARG APPLICATION_SERVER_PORT=8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/ \
    VIRTUAL_ENVIRONMENT_PATH="/app/.venv" \
    APPLICATION_SERVER_PORT=$APPLICATION_SERVER_PORT

ENV PATH="$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"
WORKDIR ${PYTHONPATH}
COPY ./requirements/prod.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app
EXPOSE ${APPLICATION_SERVER_PORT}
CMD ["sh", "-c", "cd app && python main.py"]
