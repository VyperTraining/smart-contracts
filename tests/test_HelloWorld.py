def test_hello_world(hello_world_contract):
    assert hello_world_contract.greet() == 'Hello World!'