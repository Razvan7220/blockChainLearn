from brownie import accounts, config, SimpleStorage

def deploy_simple_storage():
    account =accounts.load("myMetamask-account")
    print(account)


def main():
    deploy_simple_storage()