from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.mongo.task import Task
from src.config import settings
from loguru import logger


async def init_mongo() -> None:
    try:
        client = AsyncIOMotorClient(
            f"mongodb://{settings.mongo_user}:{settings.mongo_password}"
            f"@localhost:27018/"
            f"?authSource=admin&retryWrites=true&w=majority"
        )

        await init_beanie(
            database=client.task_db,
            document_models=[Task],
        )

    except Exception as e:
        logger.error(f"Не смогли подключится к MongoDB: {e}")
        raise
