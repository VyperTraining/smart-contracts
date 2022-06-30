import pytest
from ape.utils import misc


@pytest.fixture
def greet(hello_world_contract):
    def greet_function(sender, message):
        price = hello_world_contract.price()
        hello_world_contract.setGreeting(message, sender=sender, value=price)
        assert hello_world_contract.greet() == "Hello " + message
        assert hello_world_contract.lastChanger() == sender

    return greet_function


def test_default_greeting(hello_world_contract):
    assert hello_world_contract.greet() == "Hello World!"


def test_set_greeting(hello_world_contract, owner, bob, greet):
    assert hello_world_contract.greet() == "Hello World!"
    assert hello_world_contract.lastChanger() == misc.ZERO_ADDRESS

    price = hello_world_contract.price()

    greet(owner, "Mars!")
    greet(bob, "Earth!")

    assert hello_world_contract.balance == price * 3


def test_withdraw(hello_world_contract, owner, bob, greet):
    greet(bob, "Mars!")

    ownerBalance = owner.balance
    hello_world_contract.withdraw(sender=bob)
    assert owner.balance > ownerBalance
    assert hello_world_contract.balance == 0
