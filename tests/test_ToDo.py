import pytest


@pytest.fixture()
def create_task(todo_contract):
    def create_task(_status, _description, _owner):
        todo_contract.createTask(_status, _description, sender=_owner)
        return todo_contract.totalTasks()

    return create_task


def test_create_task(todo_contract, owner, create_task):
    description = "write more tests"

    assert todo_contract.totalTasks() == 0

    create_task(0, description, owner)

    assert todo_contract.totalTasks() == 1
    assert todo_contract.totalUserTasks(owner) == 1

    taskId = todo_contract.userTaskAt(owner, 0)
    assert taskId == 1

    task = todo_contract.idToTask(taskId)
    assert task.description == description
    assert task.status == 0
    assert task.owner == owner
    assert task.taskId == taskId


def test_update_task_status(todo_contract, owner, create_task):
    taskId = create_task(0, "Exercise!", owner)

    task = todo_contract.idToTask(taskId)
    assert task.status == 0

    todo_contract.updateStatus(1, taskId, sender=owner)

    task = todo_contract.idToTask(taskId)
    assert task.status == 1


def test_update_task_description(todo_contract, owner, create_task):
    description = "Exercise!"
    taskId = create_task(0, description, owner)

    task = todo_contract.idToTask(taskId)
    assert task.description == description

    description = "Eat more!"
    todo_contract.updateDescription(description, taskId, sender=owner)

    task = todo_contract.idToTask(taskId)
    assert task.description == description
