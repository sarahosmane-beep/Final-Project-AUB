from fastapi import APIRouter, HTTPException, Query, Response, status

from app.models.task import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.storage.task_store import task_store


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate) -> Task:
    return task_store.create(data)


@router.get("", response_model=list[Task])
def list_tasks(
    task_status: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
) -> list[Task]:
    tasks = task_store.list()
    if task_status is not None:
        tasks = [task for task in tasks if task.status == task_status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = task_store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate) -> Task:
    task = task_store.update(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    if not task_store.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
