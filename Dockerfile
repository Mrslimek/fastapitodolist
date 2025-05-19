FROM python:3.12-alpine

RUN mkdir app_root

WORKDIR /app_root

COPY . .

RUN pip install uv && uv sync && chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
