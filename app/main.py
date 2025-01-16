from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from .routers import orders
from .database import engine, Base

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Order Service", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(
    orders.router,
    prefix="/orders",
    tags=["orders"]
)

@app.on_event("startup")
def startup():
    # Создаем таблицы в базе данных
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup complete")

@app.on_event("shutdown")
def shutdown():
    # Закрываем соединения с базой данных
    engine.dispose()
    logger.info("Application shutdown complete")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
