from brownie import FundMe

from .utils import get_account

def fund():
    account = get_account()
    fund_me = FundMe[-1]
    # print(fund_me.getPrice())
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    fund_me.fund(True, {
        "from": account,
        "value": entrance_fee
    })

def withdraw():
    account = get_account()
    fund_me = FundMe[-1]
    fund_me.withdraw({
        "from": account,
    })


def main():
    fund()
