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
