from ape import accounts, project


def main():
    deployer = accounts.load("ganache0")
    deployer.deploy(project.Token, 10000, "Vyper Training Token", "VTT", 18)
