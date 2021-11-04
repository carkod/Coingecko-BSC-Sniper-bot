from web3 import Web3
import json, requests
import settingparser as sp

class Txn_bot():
    def __init__(self, token_address):
        self.w3 = self.connect()
        self.WBNB = Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")
        self.BUSD = Web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")
        self.address = Web3.toChecksumAddress(sp.GetAddress())
        self.private_key = sp.GetSecretKey()
        self.token_address = Web3.toChecksumAddress(token_address)
        self.token_contract = self.set_token_contract()
        self.router_address, self.router = self.set_router()
        self.BUSD_contract = self.set_BUSD_contract()
        self.gas_price = sp.GetGasPrice() * (10**9)

    def connect(self):
        w3 = Web3(Web3.HTTPProvider(sp.GetRPC()))
        return w3

    def get_token_decimals(self):
        return self.token_contract.functions.decimals().call()

    def get_token_symbol(self):
        return self.token_contract.functions.symbol().call()

    def get_token_name(self):
        return self.token_contract.functions.name().call()

    def set_router(self):
        router_address = Web3.toChecksumAddress("0xde937d83e62764c1f4809b87d4c8c5779c351fbf") 
        with open("./ABIS/BSC_Swapper.json") as f:
            contract_abi = json.load(f)
        router = self.w3.eth.contract(address=router_address, abi=contract_abi)
        return router_address, router

    def set_token_contract(self):
        with open("./ABIS/bep20_abi_token.json") as f:
            contract_abi = json.load(f)
        token_contract = self.w3.eth.contract(address=self.token_address, abi=contract_abi)
        return token_contract

    def set_BUSD_contract(self):
        with open("./ABIS/bep20_abi_token.json") as f:
            contract_abi = json.load(f)
        token_contract = self.w3.eth.contract(address=self.BUSD, abi=contract_abi)
        return token_contract

    def get_token_balance(self): 
        return self.token_contract.functions.balanceOf(self.address).call() / (10 ** self.token_contract.functions.decimals().call())


    def getOutputfromTokentoBUSD(self):
        AmountBUSD = self.router.functions.getOutputfromTokentoBUSD(
            self.token_contract.functions.balanceOf(self.address).call(),
            self.token_address
            ).call()
        return float(Web3.fromWei(AmountBUSD,"ether"))

    def fromBNBtoToken(self):
        Amount = int(sp.GetAmountPerBuy() * (10**18))
        txn = self.router.functions.fromBNBtoToken(
            self.token_address
        ).buildTransaction(
            {'from': self.address, 
            'gas': 500000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': int(Amount)}
            )
        txn.update({ 'gas' : int(self.estimateGas(txn))})
        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("\nTX Hash:",txn.hex())
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        if txn_receipt["status"] == 1: return True,"\nBUY Transaction Successfull!"
        else: return False, "\nBUY Transaction Faild!"
    
    def fromTokentoBNB(self):
        self.approve()
        txn = self.router.functions.fromTokentoBNB(
            int(self.token_contract.functions.balanceOf(self.address).call()),
            self.token_address
        ).buildTransaction(
            {'from': self.address, 
            'gas': 550000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': 0}
            )
        txn.update({ 'gas' : int(self.estimateGas(txn))})
        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("\nSELL TOKENS :",txn.hex())
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        if txn_receipt["status"] == 1: return True,"\nSELL Transaction Successfull!" 
        else: return False, "\nSELL Transaction Faild!" 


    def estimateGas(self, txn):
        gas = self.w3.eth.estimateGas({
                    "from": txn['from'],
                    "to": txn['to'],
                    "value": txn['value'],
                    "data": txn['data']})
        gas = gas + (gas / 10) # Adding 1/10 from gas to gas!
        return gas


    def fromBUSDtoToken(self):
        self.approveBUSD()
        Amount = int(sp.GetAmountPerBuy() * (10**18))
        txn = self.router.functions.fromBUSDtoToken(
            Amount,
            self.token_address
        ).buildTransaction(
            {'from': self.address, 
            'gas': 600000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': 0}
            )
        txn.update({ 'gas' : int(self.estimateGas(txn))})
        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(  "BUY Hash:",txn.hex()  )
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        if txn_receipt["status"] == 1: return True, "BUY Transaction Successfull!"  
        else: return False,  "BUY Transaction Faild!"  


    def fromTokentoBUSD(self):
        self.approve()
        Token_Amount = self.token_contract.functions.balanceOf(self.address).call()
        txn = self.router.functions.fromTokentoBUSD(
            Token_Amount,
            self.token_address
        ).buildTransaction(
            {'from': self.address, 
            'gas': 850000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': 0}
            )
        txn.update({ 'gas' : int(self.estimateGas(txn))})
        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(  "SELL TOKENS :",txn.hex()  )
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        if txn_receipt["status"] == 1: return True, "SELL Transaction Successfull!"  
        else: return False,  "SELL Transaction Faild!"  

    def is_approve(self):
        Approve = self.token_contract.functions.allowance(self.address ,self.router_address).call()
        Aproved_quantity = self.token_contract.functions.balanceOf(self.address).call()
        if int(Approve) <= int(Aproved_quantity):
            return False
        else:
            return True

    def approve(self):
        if self.is_approve() == False:
            txn = self.token_contract.functions.approve(
                self.router_address,
                115792089237316195423570985008687907853269984665640564039457584007913129639935 # Max Approve
            ).buildTransaction(
                {'from': self.address, 
                'gas': 100000,
                'gasPrice': self.gas_price,
                'nonce': self.w3.eth.getTransactionCount(self.address), 
                'value': 0}
                )
            txn.update({ 'gas' : int(self.estimateGas(txn))})
            signed_txn = self.w3.eth.account.sign_transaction(
                txn,
                self.private_key
            )
            
            txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)   
            if txn_receipt["status"] == 1: return True, "Approve Successfull!" 
            else: return False,  "Approve Transaction Faild!" 
        else:
            return True, "Allready approved!" 

    def is_approveBUSD(self):
        Approve = self.BUSD_contract.functions.allowance(self.address ,self.router_address).call()
        Aproved_quantity = self.BUSD_contract.functions.balanceOf(self.address).call()
        if int(Approve) <= int(Aproved_quantity):
            return False
        else:
            return True

    def approveBUSD(self):
        if self.is_approveBUSD() == False:
            txn = self.BUSD_contract.functions.approve(
                self.router_address,
                115792089237316195423570985008687907853269984665640564039457584007913129639935 # Max Approve
            ).buildTransaction(
                {'from': self.address, 
                'gas': 100000,
                'gasPrice': self.gas_price,
                'nonce': self.w3.eth.getTransactionCount(self.address), 
                'value': 0}
                )
            txn.update({ 'gas' : int(self.estimateGas(txn))})
            signed_txn = self.w3.eth.account.sign_transaction(
                txn,
                self.private_key
            )
            txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)   
            if txn_receipt["status"] == 1: return True, "Approve Successfull!" 
            else: return False,  "Approve Transaction Faild!" 
        else:
            return True, "Allready approved!"