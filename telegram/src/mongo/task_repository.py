from loguru import logger
from datetime import datetime, timedelta

from .task import Task
from src.mongo import init_mongo


async def create_task(
    professor_id: int,
    description: str,
    task_name: str,
    deadline: str,
):
    await init_mongo()
    task = Task(
        professor_id=professor_id,
        description=description,
        task_name=task_name,
        deadline=deadline,
    )
    await task.insert()
    logger.info(f"CREATED TASK | Crated task  - {task.id}")
    return task


async def get_task_by_task_id(task_id: int):
    await init_mongo()
    return dict(await Task.find_one({"task_id": task_id}))


async def get_all_tasks():
    await init_mongo()
    return [task.model_dump() async for task in Task.find()]


async def get_task_by_name(task_name: str):
    await init_mongo()
    return dict(await Task.find_one({"task_name": task_name}))


async def get_today_tasks():
    await init_mongo()

    now = datetime.now()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1)

    tasks = await Task.find(
        Task.created_at >= start_of_day, Task.created_at < end_of_day
    ).to_list()

    return [task.model_dump() for task in tasks]


async def get_tasks_by_id(engineer_id: int):
    await init_mongo()
    tasks = await Task.find(Task.engineer_id == engineer_id).to_list()
    return [task.model_dump() for task in tasks]


async def update_engineer_in_task(task_id: int, engineer_id: int):
    await init_mongo()
    task = await Task.find_one(Task.task_id == task_id).update_one(
        {
            "$set": {
                "engineer_id": engineer_id,
                "started": True,
                "started_at": datetime.now(),
            }
        }
    )
    logger.info(f"UPDATE | Update engineer on task {task_id}: {engineer_id}")
    return task
