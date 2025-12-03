# FastAPI application
from fastapi import FastAPI
import asyncpg
import redis
import os

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/db")
async def db():
    try:
        # Подключаемся к PostgreSQL через имя сервиса в Docker Compose
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER", "app"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB", "appdb"),
            host=os.getenv("POSTGRES_HOST", "postgres")  # ← имя сервиса из docker-compose.yml
        )
        row = await conn.fetchval("SELECT 1")
        await conn.close()
        return {"db": row}
    except Exception as e:
        return {"db": f"error: {str(e)}"}

@app.get("/cache")
async def cache():
    try:
        # Подключаемся к Redis через имя сервиса в Docker Compose
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),  # ← имя сервиса из docker-compose.yml
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )
        r.set("pong", "ok", ex=5)
        return {"cache": r.get("pong")}
    except Exception as e:
        return {"cache": f"error: {str(e)}"}