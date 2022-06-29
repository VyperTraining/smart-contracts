import pytest


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def bob(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def hello_world_contract(owner, project):
    return owner.deploy(project.HelloWorld, "World!", "0.01 ether")
