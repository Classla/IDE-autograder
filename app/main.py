import logging

from fastapi import FastAPI, BackgroundTasks
from concurrent.futures import ThreadPoolExecutor
from app.autograder_classes import ProjectData
from app.tasks import run_docker_job


logging.basicConfig(level=logging.INFO)


app: FastAPI = FastAPI()

# Create a thread pool executor
executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)


@app.post("/input_output/")
async def upload_files(project: ProjectData, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(executor.submit, run_docker_job, "input_output")

    return {"output": "Task started"}


@app.post("/unit_test/")
async def upload_files(project: ProjectData, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(executor.submit, run_docker_job, "unit_test")

    return {"output": "Task started"}
