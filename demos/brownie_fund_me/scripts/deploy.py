from brownie import FundMe,network,config,MockV3Aggregator
from scripts.helpful_scripts import get_account, deploy_mocks


def deploy_fund_me():
    account= get_account()

    if network.show_active() in ["development", "ganache-ui", "ganache-local"]:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    else:
        # Dacă suntem pe Sepolia, luăm adresa din config
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return fund_me

def main():
    deploy_fund_me()

