from fastapi import FastAPI

from app.database import Base, engine
from app.routers import devices, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Statistics Service",
    description="Сервис сбора и анализа данных с устройств",
    version="1.0.0",
)

app.include_router(devices.router)
app.include_router(stats.router)


@app.get("/", tags=["Статус"])
def root():
    return {"status": "ok", "message": "Device Statistics Service is running"}
