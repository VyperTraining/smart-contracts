# @version 0.3.3

# 1. DECLARING INTERFACES

# 2. DECLARING EVENTS

event GreetingChanged:
    greeting: String[122]
    changer: indexed(address)

event Withdraw:
    sender: indexed(address)
    owner: indexed(address)
    value: uint256


# 3. DECLARING STORAGE VARIABLES
greeting: String[122]

price: public(uint256)

lastChanger: public(address)

owner: public(address)

# 4. DECLARING CALLS AND FUNCTIONS

@external
def __init__(_initialGreeting: String[122], _initialPrice: uint256):
    self.greeting = _initialGreeting
    self.price = _initialPrice
    self.owner = msg.sender

@external
@view
def greet() -> String[128]:
    return concat("Hello ", self.greeting)

@external
@payable
def setGreeting(_greeting: String[122]):
    assert self.price == msg.value, "You didn't pay the price!"

    self.lastChanger = msg.sender
    self.greeting = _greeting
    self.price = self.price * 2

    log GreetingChanged(_greeting, msg.sender)

@external
def withdraw():
    send(self.owner, self.balance)

    log Withdraw(msg.sender, self.owner, self.balance)