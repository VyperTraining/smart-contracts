def test_default_greeting(hello_world_contract):
    assert hello_world_contract.greet() == "Hello World!"


def test_set_greeting(hello_world_contract, owner, bob):
    assert hello_world_contract.greet() == "Hello World!"
    assert (
        hello_world_contract.lastChanger()
        == "0x0000000000000000000000000000000000000000"
    )

    price = hello_world_contract.price()

    hello_world_contract.setGreeting("Mars!", sender=owner, value=price)
    assert hello_world_contract.greet() == "Hello Mars!"
    assert hello_world_contract.lastChanger() == owner

    hello_world_contract.setGreeting("Earth!", sender=bob, value=price * 2)
    assert hello_world_contract.greet() == "Hello Earth!"
    assert hello_world_contract.lastChanger() == bob

    assert hello_world_contract.balance == price * 3

    # Withdraw
    ownerBalance = owner.balance
    hello_world_contract.withdraw(sender=bob)
    assert owner.balance > ownerBalance
    assert hello_world_contract.balance == 0
