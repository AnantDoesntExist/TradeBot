from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
import schedule
import time
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import urllib.request
from termcolor import cprint

# Put what ever api's login method your using in the below lines


bought_indicator = int(1)
price = ""
current_time = ""
sheet_cell_number = 1
current_bought_price = 0

# Prints Cool Bitcoin Text Art
cprint("                 ,.=ctE55ttt553tzs.,                               ", "green")
cprint("             ,,c5;z==!!::::  .::7:==it3>.,                         ", "green")
cprint("          ,xC;z!::::::    ::::::::::::!=c33x,                      ", "green")
cprint("        ,czz!:::::  ::;;..===:..:::   ::::!ct3.                    ", "green")
cprint("      ,C;/.:: :  ;=c!:::::::::::::::..      !tt3.                  ", "green")
cprint("     /z/.:   :;z!:::::J  :E3.  E:::::::..     !ct3.                ", "green")
cprint("   ,E;F   ::;t::::::::J  :E3.  E::.     ::.     \ttL               ", "green")
cprint("  ;E7.    :c::::F******   **.  *==c;..    ::     Jttk              ", "green")
cprint(" .EJ.    ;::::::L                   \:.   ::.    Jttl              ", "green")
cprint(" [:.    :::::::::773.    JE773zs.     I:. ::::.    It3L            ", "green")
cprint(";:[     L:::::::::::L    |t::!::J     |::::::::    :Et3            ", "green")
cprint("[:L    !::::::::::::L    |t::;z2F    .Et:::.:::.  ::[13 ", "green")
cprint("E:.    !::::::::::::L               =Et::::::::!  ::|13 ", "green")
cprint("E:.    (::::::::::::L    .......       \:::::::!  ::|i3 ", "green")
cprint("[:L    !::::      ::L    |3t::::!3.     ]::::::.  ::[13 ", "green")
cprint("!:(     .:::::    ::L    |t::::::3L     |:::::; ::::EE3 ", "green")
cprint(" E3.    :::::::::;z5.    Jz;;;z=F.     :E:::::.::::II3[            ", "green")
cprint(" Jt1.    :::::::[                    ;z5::::;.::::;3t3             ", "green")
cprint("  \z1.::::::::::l......   ..   ;.=ct5::::::/.::::;Et3L             ", "green")
cprint("   \t3.:::::::::::::::J  :E3.  Et::::::::;!:::::;5E3L              ", "green")
cprint("    cz\.:::::::::::::J   E3.  E:::::::z!     ;Zz37`               ", "green")
cprint("      \z3.       ::;:::::::::::::::;='      ./355F                 ", "green")
cprint("        \z3x.         ::~======='         ,c253F                   ", "green")
cprint("          tz3=.                      ..c5t32^                     ", "green")
cprint("             =zz3==...         ...=t3z13P^                        ", "green")
cprint("                 `*=zjzczIIII3zzztE3>*^`                           ", "green")
cprint("")
cprint("            Bitcoin Bot Has Started Working!", "green")


# Function to check if it should buy, sell or hold.
def check():
    global price
    global current_time
    global current_bought_price
    # Getting Time Setup
    now = datetime.now()
    current_time = now.strftime("%a, %d %b %Y %H:%M:%S")
    # Getting ATR, STOCH, MFI and Price of Bitcoin
    atrurl = "https://api.taapi.io/atr?secret=<secret>&exchange=binance&symbol=BTC/USDT&interval=1m"
    url = "https://api.nomics.com/v1/currencies/ticker?key=<nomics_secret>&ids=BTC&interval=1s&convert=USD&per-page=100&page=1"
    stochurl = "https://api.taapi.io/stoch?secret=<secret2>&exchange=binance&symbol=BTC/USDT&interval=1m"
    mfiurl = "https://api.taapi.io/mfi?secret=<secret3>&exchange=binance&symbol=BTC/USDT&interval=1m"
    url = (urllib.request.urlopen(url).read())
    url = url[179:189]
    atrpage = requests.get(atrurl)
    atrsoup = BeautifulSoup(atrpage.content, 'html.parser')
    x = re.findall('[0,1,2,3,4,5,6,7,8,9,.]+', str(atrsoup))
    x2 = re.findall('[0,1,2,3,4,5,6,7,8,9,.]+', str(url))
    stochpage = requests.get(stochurl)
    stochsoup = BeautifulSoup(stochpage.content, 'html.parser')
    x3 = re.findall('[0,1,2,3,4,5,6,7,8,9,.]+', str(stochsoup))
    atr = ''.join(x)
    mfipage = requests.get(mfiurl)
    mfisoup = BeautifulSoup(mfipage.content, 'html.parser')
    x4 = re.findall('[0,1,2,3,4,5,6,7,8,9,.]+', str(mfisoup))
    price = ''.join(x2)
    fast_and_slow_stoch = ''.join(x3)
    mfi = ''.join(x4)
    mfi_number = float(mfi)
    atr_number = float(atr)
    fast_stoch_number = fast_and_slow_stoch[0:2]
    fast_stoch_number_float = float(fast_stoch_number)
    # Making Sure We Only Hold 10 Dollars of BTC at a Time
    global bought_indicator
    # If market is volatile, price is low, money is going into the market and we don't already hold Bitcoin buy Bitcoin
    if atr_number > 45 and fast_stoch_number_float <= 20 and mfi_number <= 20 and bought_indicator == 1:
        # Put buy command from your brokerage api here
        print(" ------------------------------- ")
        print("You bought bitcoin at " + price)
        print("Current Time =", current_time)
        current_bought_price = price
        bought_indicator = 0
    # If market is volatile, price is low, money is going into the market and we hold Bitcoin sell Bitcoin
    if float(price) - float(current_bought_price) >= 100 and bought_indicator == 0:
        # Put sell command from your brokerage api here
        print(" ------------------------------- ")
        print("You sold bitcoin at " + price + " for profit")
        print("Total profit on this trade was " + (price - current_bought_price) * 0.00022)
        print("Current Time =", current_time)
        bought_indicator = 1
    if float(price) - float(current_bought_price) <= -500 and bought_indicator == 0:
        # Put sell command from brokerage api here
        print(" ------------------------------- ")
        print("You sold bitcoin at " + price + " to stop loss.")
        print("Total loss on this trade was " + (price - current_bought_price) * -0.00022)
        print("Current Time =", current_time)
        bought_indicator = 1


# This function logs whatever the bot does in google sheets
def log():
    global price
    global current_time
    global sheet_cell_number
    sheet_cell_number = sheet_cell_number + 1
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "<json_filename>.json"
    scopes = ['https://www.googleapis.com/auth/sqlservice.admin']
    service_account_file = 'token.json'
    creds = None
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)
    spreadsheet_id = '<Spreadsheet_Id>'
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    current_time_list = [[current_time]]
    price_list = [[price]]
    bought_status_bought = [["Bought"]]
    bought_status_not_bought = [["Not Bought"]]

    sheet.values().update(spreadsheetId=spreadsheet_id,
                          range='<SheetNameNOTSheetTitleWillBeOnBottomLeftHandCorner>!C' + (str(sheet_cell_number)) + ':C1000',
                          valueInputOption="USER_ENTERED",
                          body={"values": current_time_list}).execute()

    sheet.values().update(spreadsheetId=spreadsheet_id,
                          range='<SheetNameNOTSheetTitleWillBeOnBottomLeftHandCorner>!B' + (str(sheet_cell_number)) + ':B1000',
                          valueInputOption="USER_ENTERED",
                          body={"values": price_list}).execute()

    if bought_indicator == 0:
        sheet.values().update(spreadsheetId=spreadsheet_id,
                              range='<SheetNameNOTSheetTitleWillBeOnBottomLeftHandCorner>!D' + (str(sheet_cell_number)) + ':D1000',
                              valueInputOption="USER_ENTERED",
                              body={"values": bought_status_bought}).execute()

    else:
        sheet.values().update(spreadsheetId=spreadsheet_id,
                              range='<SheetNameNOTSheetTitleWillBeOnBottomLeftHandCorner>!D' + (str(sheet_cell_number)) + ':D1000',
                              valueInputOption="USER_ENTERED",
                              body={"values": bought_status_not_bought}).execute()


schedule.every(60).seconds.do(check)
schedule.every(60).seconds.do(log)
while True:
    schedule.run_pending()
    time.sleep(1)
