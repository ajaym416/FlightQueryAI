from databases import DatabaseURL
from starlette.config import Config
config = Config(".env")


POSTGRES_USER = config("POSTGRES_USER", cast=str, default="postgres")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default="postgres")
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str, default="postgres")

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}",
)