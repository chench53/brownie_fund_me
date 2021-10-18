from brownie import network, MockAggregatorV3, config, accounts
from web3 import Web3

FORKED_LOCAL_BLOCKCHAIN = ['mainnet-fork']
LOCAL_BLOCKCHAIN = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN or network.show_active() in FORKED_LOCAL_BLOCKCHAIN:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def deploy_mocks():
    account = get_account()
    print('depolying mocks...')
    if len(MockAggregatorV3) == 0:
        mock_aggregator =  MockAggregatorV3.deploy(DECIMALS, STARTING_PRICE, {"from": account})
    else:
        mock_aggregator = MockAggregatorV3[-1]
    price_feed_address = mock_aggregator.address
    print('mock depolyed at {}'.format(price_feed_address))
    return price_feed_address