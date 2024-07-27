import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI

from app.autograder_requests import (
    AutograderRequestBody,
    InputOutputRequestBody,
    UnitTestRequestBody,
)
from app.logging_config import logger
from app.tasks import unit_test_autograder, run_input_output_container, send_to_supabase

load_dotenv()

app: FastAPI = FastAPI()

# Create a thread pool executor
executor: ThreadPoolExecutor = ThreadPoolExecutor(
    max_workers=int(os.environ.get("MAX_CONTAINERS"))
)


def autograder_job(submission: AutograderRequestBody) -> None:
    if isinstance(submission, InputOutputRequestBody):
        result = run_input_output_container(submission)
        send_to_supabase(result, submission.block_uuid)
        logger.info("Successfully wrote to table.")
    elif isinstance(submission, UnitTestRequestBody):
        pass
    else:
        raise TypeError()


@app.get("/")
async def get() -> dict:
    """Autograding endpoint for input output"""
    return {"msg": "Autograder API"}


@app.post("/input_output/")
async def input_output(
    project: InputOutputRequestBody, background_tasks: BackgroundTasks
) -> dict:
    """Autograding endpoint for input output"""
    background_tasks.add_task(executor.submit, autograder_job, project)
    logger.info("input_output task queued.")
    return {"output": "Task queued"}


@app.post("/unit_test/")
async def unit_test(
    project: UnitTestRequestBody, background_tasks: BackgroundTasks
) -> dict:
    """Autograding endpoint for unit tests"""
    background_tasks.add_task(executor.submit, unit_test_autograder, project)

    return {"output": "Task started"}
