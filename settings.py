from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL", default="postgresql+asyncpg://ozon:ozon@localhost:5432/ozon"
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://ozon_test:ozon_test@localhost:5433/ozon_test",
)
