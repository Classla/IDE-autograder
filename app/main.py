import logging
from concurrent.futures import ThreadPoolExecutor

from fastapi import BackgroundTasks, FastAPI

from app.autograder_classes import ProjectData
from app.tasks import run_docker_job

logging.basicConfig(level=logging.INFO)


app: FastAPI = FastAPI()

# Create a thread pool executor
executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)


@app.post("/input_output/")
async def input_output(project: ProjectData, background_tasks: BackgroundTasks) -> dict:
    """Autograding endpoint for input output"""
    background_tasks.add_task(executor.submit, run_docker_job, project, "input_output")

    return {"output": "Task started"}


@app.post("/unit_test/")
async def unit_test(project: ProjectData, background_tasks: BackgroundTasks) -> dict:
    """Autograding endpoint for unit tests"""
    background_tasks.add_task(executor.submit, run_docker_job, project, "unit_test")

    return {"output": "Task started"}
