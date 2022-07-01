import pytest
import ape


def test_metadata(token_contract):
    assert token_contract.name() == "Vyper Training Token"
    assert token_contract.symbol() == "VTT"


def test_totalSupply(token_contract):
    assert token_contract.totalSupply() == 10000 * 10 ** token_contract.decimals()


def test_totalBalanceOfOwner(token_contract, owner):
    assert token_contract.balanceOf(owner) == token_contract.totalSupply()


def test_transfer(token_contract, owner, bob):
    value = 1000
    ownerBalance = token_contract.balanceOf(owner)
    token_contract.transfer(bob, value, sender=owner)
    assert token_contract.balanceOf(bob) == value
    assert token_contract.balanceOf(owner) == ownerBalance - value


def test_approval(token_contract, owner, bob):
    value = 1000

    assert token_contract.allowance(owner, bob) == 0
    token_contract.approve(bob, value, sender=owner)
    assert token_contract.allowance(owner, bob) == value


def test_transferFrom(token_contract, owner, bob):
    value = 1000

    token_contract.approve(bob, value, sender=owner)

    ownerBalance = token_contract.balanceOf(owner)

    token_contract.transferFrom(owner, bob, value, sender=bob)

    assert token_contract.balanceOf(bob) == value
    assert token_contract.balanceOf(owner) == ownerBalance - value


def test_transferFromShouldFailIfExceedsAllowance(token_contract, owner, bob, alice):
    value = 1000

    token_contract.approve(bob, value, sender=owner)

    ownerBalance = token_contract.balanceOf(owner)

    with ape.reverts():
        token_contract.transferFrom(owner, alice, value + 1, sender=bob)

    assert token_contract.balanceOf(bob) == 0
    assert token_contract.balanceOf(owner) == ownerBalance
