import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI

from app.autograder_request_bodies import (
    AutograderRequestBody,
    InputOutputRequestBody,
    UnitTestRequestBody,
)
from app.logging_config import logger
from app.tasks import (
    run_input_output_container,
    run_unit_test_container,
    send_to_supabase,
)

load_dotenv()

app: FastAPI = FastAPI()

# Create a thread pool executor
executor: ThreadPoolExecutor = ThreadPoolExecutor(
    max_workers=int(
        os.environ.get("MAX_CONTAINERS") if os.environ.get("MAX_CONTAINERS") else 1
    )
)


def autograder_job(submission: AutograderRequestBody) -> None:
    """Controller for the autograder job"""
    if isinstance(submission, InputOutputRequestBody):
        execute_container_runtime = run_input_output_container
    elif isinstance(submission, UnitTestRequestBody):
        execute_container_runtime = run_unit_test_container
    else:
        raise TypeError()

    try:
        result = execute_container_runtime(submission)
    except Exception:
        result = {
            "autograde_mode": "unit_test",
            "msg": "Autograder failed to run.",
        }

    send_to_supabase(result, submission.block_uuid)
    logger.info("Successfully wrote to table.")


@app.get("/")
async def get() -> dict:
    """Autograding endpoint for input output"""
    return {"msg": "Autograder API ver 2"}


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
    background_tasks.add_task(executor.submit, autograder_job, project)
    logger.info("unit_test task queued.")
    return {"output": "Task queued"}
