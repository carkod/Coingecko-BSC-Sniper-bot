import requests, json

class HoneyPotChecker():
    
    def __init__(self, Token_Address):
        self.url = f"https://ishoneypot.trading-tigers.com/token/{Token_Address}"
        
    def Is_Honeypot(self):
        r = requests.get(self.url)
        jres = json.loads(r.text)
        if jres['HONEYPOT']  == False:
            return False
        elif jres['HONEYPOT'] == True:
            return True

    def getTAX(self):
        r = requests.get(self.url)
        jres = json.loads(r.text)
        try:
            return jres['SELLTAX'], jres['BUYTAX']
        except:
            return 0, 0