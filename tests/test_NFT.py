import pytest

def test_mint_nft(nft_contract, bob):
    assert nft_contract.balanceOf(bob) == 0
    nft_contract.mint(bob, 10, sender=bob)
    assert nft_contract.balanceOf(bob) == 1
    assert nft_contract.ownerOf(10) == bob