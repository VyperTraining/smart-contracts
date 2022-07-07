import pytest
import ape


def test_mint_nft(nft_contract, bob):
    assert nft_contract.balanceOf(bob) == 0
    nft_contract.mint(bob, 10, sender=bob)
    assert nft_contract.balanceOf(bob) == 1
    assert nft_contract.ownerOf(10) == bob


def test_approval(nft_contract, bob, alice):
    nft_contract.mint(bob, 10, sender=bob)

    tx = nft_contract.approve(alice, 10, sender=bob)
    assert nft_contract.getApproved(10) == alice

    # test Approval event
    logs = list(tx.decode_logs(nft_contract.Approval))
    assert len(logs) == 1

    event = logs[0]
    assert event.owner == bob
    assert event.approved == alice
    assert event.tokenId == 10

    assert nft_contract.balanceOf(bob) == 1
    tx = nft_contract.transferFrom(bob, alice, 10, sender=alice)

    # test Transfer event
    logs = list(tx.decode_logs(nft_contract.Transfer))
    assert len(logs) == 1

    event = logs[0]
    assert event.sender == bob
    assert event.receiver == alice
    assert event.tokenId == 10

    assert nft_contract.balanceOf(bob) == 0
    assert nft_contract.balanceOf(alice) == 1
    assert nft_contract.ownerOf(10) == alice


def test_approval_for_all(nft_contract, bob, alice, owner):
    nft_contract.mint(alice, 10, sender=alice)
    nft_contract.mint(alice, 11, sender=alice)
    assert nft_contract.balanceOf(alice) == 2

    tx = nft_contract.setApprovalForAll(bob, True, sender=alice)
    assert nft_contract.isApprovedForAll(alice, bob) == True

    # test ApprovalForAll
    logs = list(tx.decode_logs(nft_contract.ApprovalForAll))
    assert len(logs) == 1

    event = logs[0]
    assert event.owner == alice
    assert event.operator == bob
    assert event.approved == True

    nft_contract.transferFrom(alice, owner, 10, sender=bob)
    assert nft_contract.balanceOf(owner) == 1

    with ape.reverts():
        nft_contract.transferFrom(owner, alice, 10, sender=bob)

    nft_contract.setApprovalForAll(bob, True, sender=owner)
    assert nft_contract.isApprovedForAll(owner, bob) == True

    nft_contract.transferFrom(owner, alice, 10, sender=bob)
    assert nft_contract.balanceOf(owner) == 0


def test_approval_for_all(nft_contract, bob, alice, owner):
    nft_contract.mint(alice, 10, sender=alice)
    nft_contract.mint(alice, 11, sender=alice)
    assert nft_contract.balanceOf(alice) == 2

    nft_contract.setApprovalForAll(bob, True, sender=alice)
    assert nft_contract.isApprovedForAll(alice, bob) == True

    nft_contract.transferFrom(alice, owner, 10, sender=bob)
    assert nft_contract.balanceOf(owner) == 1

    nft_contract.setApprovalForAll(bob, False, sender=alice)
    assert nft_contract.isApprovedForAll(alice, bob) == False

    with ape.reverts():
        nft_contract.transferFrom(alice, bob, 11, sender=bob)


def test_approval_revoke_on_transfer(nft_contract, bob, alice, owner):
    nft_contract.mint(bob, 12, sender=bob)

    nft_contract.approve(alice, 12, sender=bob)
    assert nft_contract.getApproved(12) == alice

    nft_contract.transferFrom(bob, owner, 12, sender=alice)
    assert nft_contract.balanceOf(bob) == 0
    assert nft_contract.balanceOf(owner) == 1

    assert nft_contract.getApproved(12) != alice  # == ZERO_ADDRESS gives same result
    with ape.reverts():
        nft_contract.transferFrom(owner, bob, 12, sender=alice)

    nft_contract.approve(alice, 12, sender=owner)
    assert nft_contract.getApproved(12) == alice

    nft_contract.transferFrom(owner, bob, 12, sender=alice)
    assert nft_contract.balanceOf(bob) == 1
    assert nft_contract.balanceOf(owner) == 0


def test_transfer_to_contract(nft_contract, bob, receiver_contract):
    nft_contract.mint(bob, 12, sender=bob)
    assert nft_contract.balanceOf(bob) == 1
    assert nft_contract.balanceOf(receiver_contract) == 0
    assert nft_contract.ownerOf(12) == bob

    nft_contract.safeTransferFrom(bob, receiver_contract, 12, sender=bob)
    assert nft_contract.balanceOf(bob) == 0
    assert nft_contract.balanceOf(receiver_contract) == 1
    assert nft_contract.ownerOf(12) == receiver_contract

    receiver_contract.returnToken(nft_contract, 12, sender=bob)
    assert nft_contract.balanceOf(bob) == 1
    assert nft_contract.balanceOf(receiver_contract) == 0
    assert nft_contract.ownerOf(12) == bob
