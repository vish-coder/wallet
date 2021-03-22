#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pprint
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pathlib import Path
from getpass import getpass
import subprocess
import json
from constants import *


# In[2]:


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# In[3]:


load_dotenv()
mnemo=os.getenv("MNEMONIC")
# print(mnemo)


# In[4]:


# command = 'php ./derive -g --mnemonic="foam disorder sort unhappy security awkward soldier fault mirror judge pigeon sock face real plug" --cols=all --coin=BTCTEST  --numderive=4 --format=json'  
# p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,text=True)
# output, err = p.communicate()
# p_status = p.wait()
# # keys = json.loads(output)
# keys = print(json.dumps(output, sort_keys=True, indent=4))
# print(keys)
#     #return (keys)


# In[5]:


# command = 'php ./derive -g --mnemonic="foam disorder sort unhappy security awkward soldier fault mirror judge pigeon sock face real plug" --cols=all --coin=btc-test --numderive=4 --format=json'
# p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# output, err = p.communicate()
# p_status = p.wait()
# keys = json.loads(output)
# # keys = print(json.dumps(output, sort_keys=True, indent=4))
# print(keys)
#     #return (keys)


# In[6]:


# def derive_wallets(nemo,koin,numd):
# def derive_wallets(nemo,numd):
def derive_wallets_btc(nemo):
#     command='php ./derive -g --mnemonic=nemo --coin=koin --numderive=numd --cols=all --format=json'
#     command='php ./derive -g --mnemonic=nemo --coin=BTC --numderive=numd --cols=all --format=json'
    command='php ./derive -g --mnemonic=nemo --coin=btc-test --numderive=4 --cols=all --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return (keys)


# In[7]:


# derive_wallets(mnemo,'BTC',4)
# derive_wallets(mnemo,4)
# derive_wallets_btc(mnemo)


# In[8]:


def derive_wallets_eth(nemo):
#     command='php ./derive -g --mnemonic=nemo --coin=koin --numderive=numd --cols=all --format=json'
#     command='php ./derive -g --mnemonic=nemo --coin=BTC --numderive=numd --cols=all --format=json'
    command='php ./derive -g --mnemonic=nemo --coin=eth --numderive=4 --cols=all --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return (keys)


# In[9]:


# derive_wallets_eth(mnemo)


# In[10]:


coins = {}
coins['btc-test']=derive_wallets_btc(mnemo)
coins['eth']=derive_wallets_eth(mnemo)
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(coins)


# In[11]:


from constants import *
from bit import PrivateKeyTestnet
def priv_key_to_account(coin):
    priv_key=coins[coin][1]['privkey']
    if coin==ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin==BTCTEST:
        return PrivateKeyTestnet(priv_key)
    else:
        return exception


# In[12]:


btc_key=coins[BTCTEST][1]['privkey'] 
eth_key=coins[ETH][1]['privkey']
# btc_key, eth_key


# In[13]:


btc_acc= priv_key_to_account(BTCTEST)
eth_acc= priv_key_to_account(ETH)
# btc_acc, eth_acc


# In[14]:


from bit.network import NetworkAPI, satoshi_to_currency
from bit import wif_to_key


# In[18]:


# # bit.get_balance(currency='BTCTEST')
# satoshi_to_currency(NetworkAPI.get_balance_testnet(btc_acc.address), BTC)
# create_raw_tx(ETH,'0x2BD53FF41fdB7e3fE32d322A74a20c9F1526C0d9','0x65945FB0765AC2D697944C89F6C9838c8138d4e2',0.0001)
# w3.getBalance("0x2BD53FF41fdB7e3fE32d322A74a20c9F1526C0d9")


# In[19]:


def create_raw_tx(coin,account,recipient,amount):
    if coin==ETH:
        gasEstimate = w3.eth.estimateGas({"from": account.address, "to": recipient, "value": w3.toWei(amount,'ether') })
        return {"from": account.address,
                "to": recipient,
                "value": w3.toWei(amount,'ether'),
                "gasPrice": w3.eth.gasPrice,
                "gas": gasEstimate,
                "nonce": w3.eth.getTransactionCount(account.address)}
    elif coin==BTCTEST:
            return PrivateKeyTestnet.prepare_transaction(account,[(recipient,amount,BTC)])
    else:
            return exception


# In[ ]:


# from bit import wif_to_key
# key = wif_to_key(btc_key)
# recipient="mpb24ycj5jEKjfLaBmwnFD5T6iLY2SHDpK"
# key
# outputs = []
# outputs.append((address, 0.001, "btc"))
# print(key.send(outputs))


# In[ ]:


def send_tx(coin,account,recipient,amount):
    if coin==ETH:
            tx = create_raw_tx(coin,account,recipient,amount)
            key = wif_to_key(eth_key)
            signed_tx = key.sign_transaction(tx)
            result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(result)
            return (result)
    elif coin==BTCTEST:
            tx = create_raw_tx(coin,account,recipient,amount)
            key = wif_to_key(btc_key)
            signed_tx = key.sign_transaction(tx)
            result=NetworkAPI.broadcast_tx_testnet(signed_tx)
            print(result)
            return(result)
    else:
            return exception


# In[ ]:





# In[ ]:




