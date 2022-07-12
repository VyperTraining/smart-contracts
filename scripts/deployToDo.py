from ape import accounts, project


def main():
    deployer = accounts.load("deployer")
    deployer.deploy(project.ToDo)
