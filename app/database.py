from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()

# Build the connection string
# Ưu tiên lấy DATABASE_URL trực tiếp từ .env hoặc biến môi trường
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Nếu không có DATABASE_URL, tự xây dựng từ các thành phần lẻ
    # Mặc định sử dụng thông tin Neon Postgres Online
    DB_USER = os.getenv("DB_USER", "neondb_owner")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "npg_tmPI1Fqj0Eoz")
    DB_HOST = os.getenv("DB_HOST", "ep-misty-silence-anrn45w0-pooler.c-6.us-east-1.aws.neon.tech")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "neondb")
    
    # Đảm bảo dùng driver asyncpg cho SQLAlchemy Async
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl=require"
else:
    # Nếu đã có DATABASE_URL, đảm bảo nó sử dụng driver asyncpg
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    if "ssl=require" not in DATABASE_URL and "sslmode=require" not in DATABASE_URL:
        connector = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL += f"{connector}ssl=require"
    elif "sslmode=require" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("sslmode=require", "ssl=require")

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
