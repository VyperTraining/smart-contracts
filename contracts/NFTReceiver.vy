# @version 0.3.3

# 1. DECLARING INTERFACES

# Interface for the contract called by safeTransferFrom()
from vyper.interfaces import ERC721

interface ERC721Receiver:
    def onERC721Received(
            _operator: address,
            _from: address,
            _tokenId: uint256,
            _data: Bytes[1024]
        ) -> bytes32: view

implements: ERC721Receiver

# 2. DECLARING EVENTS

# 3. DECLARING STORAGE VARIABLES
ownerOf: public(HashMap[address, HashMap[uint256, address]])

# 4. DECLARING CALLS AND FUNCTIONS
@nonpayable
@external
def onERC721Received( _operator: address, _from: address, _tokenId: uint256, _data: Bytes[1024]=b"") -> bytes32:
    assert ERC721(msg.sender).ownerOf(_tokenId) == _from

    self.ownerOf[msg.sender][_tokenId] = _from

    return method_id("onERC721Received(address,address,uint256,bytes)", output_type=bytes32)

@nonpayable
@external
def returnToken(contract_address: address, _tokenId: uint256):
    owner: address = self.ownerOf[contract_address][_tokenId]
    assert msg.sender == owner

    nft_contract: ERC721 = ERC721(contract_address)
    nft_contract.safeTransferFrom(self, owner, _tokenId, b"")
