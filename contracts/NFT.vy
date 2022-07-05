# @version 0.3.3

# 1. DECLARING INTERFACES

from vyper.interfaces import ERC721

implements: ERC721

# Interface for the contract called by safeTransferFrom()
interface ERC721Receiver:
    def onERC721Received(
            _operator: address,
            _from: address,
            _tokenId: uint256,
            _data: Bytes[1024]
        ) -> bytes32: view

# 2. DECLARING EVENTS

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    tokenId: indexed(uint256)

event Approval:
    owner: indexed(address)
    approved: indexed(address)
    tokenId: indexed(uint256)

event ApprovalForAll:
    owner: indexed(address)
    operator: indexed(address)
    approved: bool


# 3. DECLARING STORAGE VARIABLES

ownerOf: public(HashMap[uint256, address])
# ---> def ownerOf(_tokenId: uint256) -> address:
balanceOf: public(HashMap[address, uint256])
# ---> def balanceOf(_owner: address) -> uint256:
getApproved: public(HashMap[uint256, address])
# ---> def getApproved(_tokenId: uint256) -> address:
isApprovedForAll: public(HashMap[address, HashMap[address, bool]])
# ---> def isApprovedForAll(_owner: address, _operator: address) -> bool:


# 4. DECLARING CALLS AND FUNCTIONS

@view
@internal
def _hasPermission(_sender: address, _tokenId: uint256) -> bool:
    owner: address = self.ownerOf[_tokenId]
    senderIsOwner: bool = owner == _sender
    senderIsApproved: bool = self.getApproved[_tokenId] == _sender
    senderIsApprovedAll: bool = self.isApprovedForAll[owner][_sender]

    return senderIsOwner or senderIsApproved or senderIsApprovedAll

@internal
def _clearApproval(_owner: address, _tokenId: uint256):
    assert _owner == self.ownerOf[_tokenId]

    if self.getApproved[_tokenId] != ZERO_ADDRESS:
       self.getApproved[_tokenId] = ZERO_ADDRESS

@internal
def _removeTokenFromOwner(_owner: address, _tokenId: uint256):
    assert _owner == self.ownerOf[_tokenId]
    self.ownerOf[_tokenId] = ZERO_ADDRESS
    self.balanceOf[_owner] -= 1

@internal
def _addTokenToOwner(_to: address, _tokenId: uint256):
    assert self.ownerOf[_tokenId] == ZERO_ADDRESS
    self.ownerOf[_tokenId] = _to
    self.balanceOf[_to] += 1

@internal
def _transferFrom(_from: address, _to: address, _tokenId: uint256, _sender: address):
    # 1 - Check permission
    assert self._hasPermission(_sender, _tokenId)
    assert _to != ZERO_ADDRESS # Not required but important if you don't want to burn tokens

    # 2 - Clear the approval
    self._clearApproval(_from, _tokenId)

    # 3 - Change Ownership
    self._removeTokenFromOwner(_from, _tokenId)
    self._addTokenToOwner(_to, _tokenId)
    
    log Transfer(_from, _to, _tokenId)

@nonpayable
@external
def transferFrom(_from: address, _to: address, _tokenId: uint256):
    self._transferFrom(_from, _to, _tokenId, msg.sender)
    

@nonpayable
@external
def safeTransferFrom(_from: address, _to: address, _tokenId: uint256, _data: Bytes[1024]=b""):
    self._transferFrom(_from, _to, _tokenId, msg.sender)
    if _to.is_contract: # check if `_to` is a contract address
        returnValue: bytes32 = ERC721Receiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data)
        # Throws if transfer destination is a contract which does not implement 'onERC721Received'
        assert returnValue == method_id("onERC721Received(address,address,uint256,bytes)", output_type=bytes32)
  
@nonpayable
@external
def approve(_approved: address, _tokenId: uint256):
    owner: address = self.ownerOf[_tokenId]

    assert owner != ZERO_ADDRESS
    assert owner != _approved

    senderIsOwner: bool = msg.sender == owner
    senderIsApprovedAll: bool = self.isApprovedForAll[owner][msg.sender]

    assert senderIsOwner or senderIsApprovedAll

    self.getApproved[_tokenId] = _approved

    log Approval(msg.sender, _approved, _tokenId)

@nonpayable
@external
def setApprovalForAll(_operator: address, _approved: bool):
    assert _operator != msg.sender
    
    self.isApprovedForAll[msg.sender][_operator] = _approved

    log ApprovalForAll(msg.sender, _operator, _approved)

@nonpayable
@external
def mint(_to: address, _tokenId: uint256):
    self._addTokenToOwner(_to, _tokenId)