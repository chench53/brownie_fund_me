from brownie import FundMe, network, config

from .utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN

def deploy_fund_me():
    account = get_account()
    # print(account)
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        price_feed_address = config['networks'][network.show_active()]['price_feed_address']
    else:
        price_feed_address = deploy_mocks()

    fund_me = FundMe.deploy(
        price_feed_address, 
        {"from": account}, 
        publish_source=config['networks'][network.show_active()].get('verify')
    )
    print("FundMe deployed at {}".format(fund_me.address))
    return fund_me

def main():
    deploy_fund_me()