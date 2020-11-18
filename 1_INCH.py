import configparser 
import requests
import os
import json
import web3
from web3 import Web3
from time import sleep
import web3
import configparser
import click
# импортируем библиотеку

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("wallet_sender.ini") 
if not type(config.read("wallet_sender.ini") ):
    print('OOPS')
else:
    print(config.read("wallet_sender.ini"))
try:
    infura = config['SENDER']['INFURA'] #Инфура
    w3 = Web3(Web3.HTTPProvider(infura))
    my_wallet = config['SENDER']['MY_WALLET']#Кошелек для отправки эфира
    my_private_key = config['SENDER']['MY_PRIVATE_KEY']#Приватный
    am_eth = float(config['SENDER']['AMOUNT_ETH'])#Кол-во эфира 
    gas_price = int(config['SENDER']['GAS_PRICE'])
    AMOUNT_FOR_WETH = float(config['INCH']['AMOUNT_FOR_WETH'])
    if config.read("wallet_sender.ini"):
        try:    
            with open ("wallets") as f:
                wallets = [line.rstrip() for line in f]    
            with open ("private_keys") as p:
                private_keys = [line.rstrip() for line in p]
                if wallets and private_keys and len(wallets)==len(private_keys):
                    summ_eth  = am_eth*len(wallets)
                    if click.confirm('Вы хотите отправить %sETH по %s ETH на %s кошельков'%(summ_eth,am_eth,len(wallets)), default=True):
                        wallets_2=[]
                        for i in wallets:
                            d = w3.toChecksumAddress(i)
                            wallets_2.append(d)
                        am = w3.toWei(am_eth, 'ether')
                        nonce = w3.eth.getTransactionCount(w3.toChecksumAddress(my_wallet))
                        for i in wallets_2:
                            try:
                                txn =dict({
                                     'gas': 21000,
                                     'gasPrice': w3.toWei(gas_price,'GWEI'),
                                     'to':i,
                                     'value': am,
                                     'nonce': nonce,

                                })
                                signed_txn = w3.eth.account.sign_transaction(txn, private_key=my_private_key)
                                tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                                nonce +=1
                                print(tx_hash.hex()) 
                            except:
                                print('OOPS Check:', i)
                        print('Выполнено, Ожидайте...')
                        receipt = w3.eth.waitForTransactionReceipt(tx_hash,timeout=None)
                        
                        if receipt:
                            
                            if click.confirm('Вы хотите обменять %s ETH на WETH ' % AMOUNT_FOR_WETH, default=True):
                                am_weth = w3.toWei(AMOUNT_FOR_WETH, 'ether')
                                for wallet, private_key in zip(wallets_2,private_keys):
                                    try:
                                        url = 'https://api.1inch.exchange/v1.1/swap?fromTokenSymbol=ETH&toTokenSymbol=WETH&amount=%s&fromAddress=%s&slippage=1&disableEstimate=true'%(am_weth,wallet)
                                        response = requests.get(url)
                                        nonce = w3.eth.getTransactionCount(wallet)
                                        txn = response.json()
                                        #print(url)
                                        #txn['gas'] = int(int(txn['gas'])/10)
                                        txn['gas'] = int(250000)
                                        txn['gasPrice'] = int(txn['gasPrice'])
                                        txn['value'] = int(txn['value'])
                                        txn['nonce'] = int(nonce)
                                        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
                                        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                                        print(tx_hash.hex())

                                    except:
                                        print('OOPS Check:', wallet)  
                                print('Выполнено')
                    else:
                        wallets_2=[]
                        for i in wallets:
                            d = w3.toChecksumAddress(i)
                            wallets_2.append(d)
                        if click.confirm('Вы хотите обменять %s ETH на WETH ' %AMOUNT_FOR_WETH, default=True):
                            am_weth = w3.toWei(AMOUNT_FOR_WETH, 'ether')
                            for wallet, private_key in zip(wallets_2,private_keys):
                                try:
                                    url = 'https://api.1inch.exchange/v1.1/swap?fromTokenSymbol=ETH&toTokenSymbol=WETH&amount=%s&fromAddress=%s&slippage=1&disableEstimate=true'%(am_weth,wallet)
                                    response = requests.get(url)
                                    nonce = w3.eth.getTransactionCount(wallet)
                                    txn = response.json()
                                    #print(url)
                                    #txn['gas'] = int(int(txn['gas'])/10)
                                    txn['gas'] = int(250000)
                                    txn['gasPrice'] = int(txn['gasPrice'])
                                    txn['value'] = int(txn['value'])
                                    txn['nonce'] = int(nonce)
                                    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
                                    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                                    print(tx_hash.hex())

                                except:
                                    print('OOPS Check:', wallet)  
                            print('Выполнено')
            
        except:
            print('Проверьте наличие файлов wallets и private_keys')
                    
                
except:
    print('Проверьте заполненность всех полей файла wallet_sender.ini')
