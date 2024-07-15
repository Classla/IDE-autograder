import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI

from app.autograder_classes import InputOutputRequestBody, UnitTestRequestBody
from app.logging_config import logger
from app.tasks import input_output_autograder, unit_test_autograder

load_dotenv()

app: FastAPI = FastAPI()

# Create a thread pool executor
executor: ThreadPoolExecutor = ThreadPoolExecutor(
    max_workers=int(os.environ.get("MAX_CONTAINERS"))
)


@app.post("/input_output/")
async def input_output(
    project: InputOutputRequestBody, background_tasks: BackgroundTasks
) -> dict:
    """Autograding endpoint for input output"""
    background_tasks.add_task(executor.submit, input_output_autograder, project)
    logger.info("input_output task queued.")
    return {"output": "Task queued"}


@app.post("/unit_test/")
async def unit_test(
    project: UnitTestRequestBody, background_tasks: BackgroundTasks
) -> dict:
    """Autograding endpoint for unit tests"""
    background_tasks.add_task(executor.submit, unit_test_autograder, project)

    return {"output": "Task started"}
