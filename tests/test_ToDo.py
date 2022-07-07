import pytest


def test_create_task(todo_contract, owner):
    description = "write more tests"

    assert todo_contract.totalTasks() == 0

    todo_contract.createTask(0, description, sender=owner)

    assert todo_contract.totalTasks() == 1
    assert todo_contract.totalUserTasks(owner) == 1

    taskId = todo_contract.userTaskAt(owner, 0)
    assert taskId == 1

    task = todo_contract.idToTask(taskId)
    assert task.description == description
    assert task.status == 0
    assert task.owner == owner
    assert task.taskId == taskId
