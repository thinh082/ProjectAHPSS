from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()

# Build the connection string
# Theo thông tin bạn cung cấp:
# Host: localhost, Port: 5432, DB: myserver, user: postgres, pass: thinh123
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "thinh123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ahp_samsung")

# Database URL cho kết nối bất đồng bộ (asyncpg)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine bất đồng bộ
engine = create_async_engine(DATABASE_URL, echo=True)

# Session local
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base class cho các ORM model
Base = declarative_base()

# Dependency để sử dụng trong các route FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
