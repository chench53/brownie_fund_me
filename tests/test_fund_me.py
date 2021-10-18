import pytest

from brownie import FundMe, network, config, accounts, exceptions

from scripts.utils import get_account
from scripts.deploy import deploy_fund_me
from scripts.utils import LOCAL_BLOCKCHAIN

def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 1000
    tx = fund_me.fund(True, {
        "from": account,
        "value": entrance_fee
    })
    tx.wait(1)
    assert fund_me.a2v(account.address) == entrance_fee
    tx = fund_me.withdraw({
        "from": account,
    })
    tx.wait(1)
    assert fund_me.a2v(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN :
        pytest.skip("only for local testing")
    # account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({
            "from": bad_actor,
        })
