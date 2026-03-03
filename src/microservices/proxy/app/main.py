import os
import random
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx
from typing import Dict, Any

# Чтение переменных окружения
PORT = int(os.getenv("PORT", 8000))
#MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:8888")  #--- TODO: 8080 -> 8888 I.A.
MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:8080")  #--- TODO: I.A. 2026-03-04
MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "http://movies-service:8081")
EVENTS_SERVICE_URL = os.getenv("EVENTS_SERVICE_URL", "http://events-service:8082")
GRADUAL_MIGRATION = os.getenv("GRADUAL_MIGRATION", "false").lower() == "true"
MOVIES_MIGRATION_PERCENT = int(os.getenv("MOVIES_MIGRATION_PERCENT", "0"))

app = FastAPI(title="Strangler Fig Proxy")

# HTTP-клиент для проксирования
client = httpx.AsyncClient(timeout=30.0)

# Список заголовков, которые не нужно передавать дальше
HOP_BY_HOP_HEADERS = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "content-length", "host"
}

def should_route_to_movies_service() -> bool:
    """Определяет, должен ли запрос к movies идти в новый сервис."""
    if not GRADUAL_MIGRATION:
        return False
    # Случайное число от 0 до 99
    return random.randint(0, 99) < MOVIES_MIGRATION_PERCENT

def filter_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Убирает служебные заголовки."""
    return {k: v for k, v in headers.items() if k.lower() not in HOP_BY_HOP_HEADERS}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str):
    """
    Универсальный прокси-обработчик.
    Определяет целевой сервис по пути запроса и правилам миграции.
    """
    # Определяем базовый URL
    if path.startswith("api/movies"):
        if should_route_to_movies_service():
            base_url = MOVIES_SERVICE_URL
        else:
            base_url = MONOLITH_URL
    elif path.startswith("api/events"):
        base_url = EVENTS_SERVICE_URL
    else:
        base_url = MONOLITH_URL

    # Формируем полный URL
    query = request.url.query
    url = f"{base_url}/{path}"
    if query:
        url += f"?{query}"

    # Подготавливаем тело запроса
    body = await request.body()

    # Фильтруем заголовки
    headers = filter_headers(dict(request.headers))

    try:
        # Выполняем запрос к целевому сервису
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body if body else None,
        )
        # Возвращаем ответ клиенту
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=filter_headers(dict(resp.headers)),
        )
    except Exception as e:
        # В случае ошибки возвращаем 502 Bad Gateway
        return JSONResponse(
            status_code=502,
            content={"error": "Bad Gateway", "detail": str(e)},
        )

@app.on_event("shutdown")
async def shutdown():
    await client.aclose()