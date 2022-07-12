from ape import project
import json
import os

path = "./abis/"

def writeAbi(Contract):
    contractName = Contract.name

    print("Generating ABIs for " + contractName)
    print("===========================================")

    abi = {"abi": [abi.dict() for abi in Contract.abi]}
    with open(path + contractName + ".json", "w") as outfile:
        json.dump(abi, outfile, indent=2)


def main():
    if not os.path.exists(path):
        os.makedirs(path)

    for contract in project.contracts:
        writeAbi(project.contracts[contract])
