import json
import time
from requests_html import HTMLSession
from hpcheck import HoneyPotChecker
import settingparser as sp
from log import logbook
from tx import Txn_bot
from threading import Thread as T

session = HTMLSession()
INFO = logbook().createINFOLogger()
ERROR = logbook().createERRORLogger()

ascii = """
  ______               ___                _______                     
 /_  __/________ _____/ (_)___  ____ _   /_  __(_)___ ____  __________
  / / / ___/ __ `/ __  / / __ \/ __ `/    / / / / __ `/ _ \/ ___/ ___/
 / / / /  / /_/ / /_/ / / / / / /_/ /    / / / / /_/ /  __/ /  (__  ) 
/_/ /_/   \__,_/\__,_/_/_/ /_/\__, /    /_/ /_/\__, /\___/_/  /____/  
                             /____/           /____/                  
"""

class TakeProfitStopLoss():

    def __init__(self, Taddress):
        self.TokenAddress = Taddress
        self.TX = Txn_bot(Taddress)
        self.TokenName = self.TX.get_token_name()
        self.TakeProfitPrice = sp.GetAmountPerBuy() + ((sp.GetAmountPerBuy()/100)*sp.GetTakeProfit())
        self.StopLostPrice = sp.GetAmountPerBuy() - ((sp.GetAmountPerBuy()/100)*sp.GetStopLost())
        self.Currency = sp.GetCurrency()
        self.START()

    def START(self):
        if self.Currency == "BUSD":
            self.STARTBUSD()
        elif self.Currency == "BNB":
            self.STARTBNB()
        else:
            print("No Supportet Currency! Only BNB or BUSD!")
        

    def STARTBUSD(self):
        try:
            if self.TX.fromBUSDtoToken()[0] == True:
                while True:
                    try:
                        time.sleep(5)
                        CurrentPrice = self.TX.getOutputfromTokentoBUSD()
                        if CurrentPrice >= self.TakeProfitPrice:
                            print(self.TX.fromTokentoBUSD()[1])
                            break
                        if CurrentPrice <= self.StopLostPrice:
                            print(self.TX.fromTokentoBUSD()[1])
                            break
                        info = str(self.TokenName) + " Current Output: " +str(round(CurrentPrice,2)) + "$"
                        INFO.info(info)
                    except Exception as e:
                        ERROR.error(e)
                        break
            else:
                e = "Buy TX FAILD!" + str(self.TokenName)
                print(e)
                ERROR.error(e)
        except Exception as e:
            ERROR.error(e)


    def STARTBNB(self):
        try:
            if self.TX.fromBNBtoToken()[0] == True:
                print("Start Thread for",self.TX.get_token_name())
                while True:
                    try:
                        time.sleep(5)
                        CurrentPrice = self.TX.getOutputfromTokentoBUSD()
                        if CurrentPrice >= self.TakeProfitPrice:
                            print(self.TX.fromTokentoBNB()[1])
                            break
                        if CurrentPrice <= self.StopLostPrice:
                            print(self.TX.fromTokentoBNB()[1])
                            break
                        info = str(self.TokenName) + " Current Output: " +str(round(CurrentPrice,2)) + " BNB"
                        INFO.info(info)
                    except Exception as e:
                        ERROR.error(e)
                        break
            else:
                e = "Buy TX FAILD!" + str(self.TokenName)
                print(e)
                ERROR.error(e)
        except Exception as e:
            ERROR.error(e)
                

class TokenScrapper():

    def __init__(self):
        self.loadBlacklist()
        
    def ScrappTokens(self):
        print(ascii)
        print("Welcome to Binance Smart Chains Coingecko Sniper bot!")
        print("If you have any questions, please join our community! \nTelegram: https://t.me/tradingTigersChat \n")
        while True:
            try:
                self.get_LastTokens()
                time.sleep(60) # Check every 60Sec Coingecko for new Tokens
            except Exception as e:
                ERROR.error(e)


    def loadBlacklist(self):
        with open("blacklist.json","r") as e:
            self.Blacklist = json.load(e)

    def saveBlacklist(self):
        with open("blacklist.json","w") as e:
            json.dump(self.Blacklist, e)

    def get_LastTokens(self):
        r = session.get('https://www.coingecko.com/en/coins/recently_added')
        f = r.html.find('tbody')
        for line in f:
            tr = line.find('tr')
            for line in tr:
                td = line.find('tr', containing='Binance')
                for line in td:
                    time = line.find('td.trade.p-0.col-market.pl-2.text-center', first=True)
                    addtime = time.text
                    a = line.find('a', first=True)
                    link = str(a.absolute_links)[+2:-2]
                    if "min" in str(addtime):
                        Taddress = str(self.get_TokenAddress(link))
                        if not Taddress in self.Blacklist:
                            print("Found new Token! Added",addtime," ago | LINK:",link)
                            self.Blacklist.append(Taddress), self.saveBlacklist()
                            SELLTAX, BUYTAX = HoneyPotChecker(Taddress).getTAX()
                            MAXTAX = sp.GetMaxTokenTax()
                            if float(SELLTAX) <= float(MAXTAX):
                                if float(BUYTAX) <= float(MAXTAX):
                                    T(target=TakeProfitStopLoss, args=[Taddress],).start()
                                        
    def get_TokenAddress(self, link):
        r = session.get(link)
        f = r.html.find('i')
        for i in f:
            if 'data-address="0x' in i.html:
               return i.html[+17:-313]


TokenScrapper().ScrappTokens()
    

