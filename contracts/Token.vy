
# @version 0.3.3

# 1. DECLARING INTERFACES

from vyper.interfaces import ERC20
from vyper.interfaces import ERC20Detailed

implements: ERC20
implements: ERC20Detailed

# 2. DECLARING EVENTS

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256 

# 3. DECLARING STORAGE VARIABLES

totalSupply: public(uint256)
balanceOf: public(HashMap[address, uint256])
# ---> def balanceOf(_owner: address) -> uint256:
allowance: public(HashMap[address, HashMap[address, uint256]])
# ----> def allowance(_owner: address, _spender: address) -> uint256:

name: public(String[32])
symbol: public(String[3])
decimals: public(uint8)


# 4. DECLARING CALLS AND FUNCTIONS

@external
def __init__(
    _totalSupply: uint256,
    _name: String[32],
    _symbol: String[3],
    _decimals: uint8
):
    finalSupply: uint256 = _totalSupply * 10 ** convert(_decimals, uint256)
    
    self.totalSupply = finalSupply
    self.balanceOf[msg.sender] = finalSupply
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals

@external
@nonpayable
def approve(_spender: address, _value: uint256) -> bool:
    self.allowance[msg.sender][_spender] = _value

    log Approval(msg.sender, _spender, _value)
    return True

@external
@nonpayable
def transfer(_to: address, _value: uint256) -> bool:

    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value

    log Transfer(msg.sender, _to, _value)
    return True

@external
@nonpayable
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    self.allowance[_from][_to] -= _value

    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value

    log Transfer(_from, _to, _value)
    return True
