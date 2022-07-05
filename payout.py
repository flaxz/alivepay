from beem import Hive
from beem import exceptions
import getpass
from hiveengine.api import Api
from hiveengine.wallet import Wallet
import pandas as pd
from time import sleep

hive = Hive(node = "https://api.deathwing.me")

setApi = Api(url = "https://engine.rishipanthee.com/")

name = input("Enter wallet name: ")

def checkHiveWallet():
    try:
        hive.wallet.getActiveKeysForAccount(name)
    except exceptions.MissingKeyError:
        key = getpass.getpass("Please Supply the Hive Wallet Active Key: ")
        try:
            hive.wallet.addPrivateKey(key)
        except exceptions.InvalidWifError:
            print("Invalid Key! Please try again.")
            checkHiveWallet()  

def unlockWallet():

    walletPassword = getpass.getpass("Wallet Password: ")
    try:
        hive.wallet.unlock(walletPassword)
    except beemstorage.exceptions.WrongMasterPasswordException:
        print("Invalid Password, please try again!")
        unlockWallet()

def payout():
  activeKey = hive.wallet.getKeyForAccount(name, "active")
  HVE = Hive(node = "https://api.deathwing.me", keys = [activeKey])
  wallet = Wallet(name, api=setApi, blockchain_instance = HVE)

  file = input("Enter CSV file name: ")

  decPoint = input("Enter decimal point(.or,): ")

  df = pd.read_csv(file, decimal = decPoint)

  df = df[::-1]

  df["amount"] = df["amount"].astype(float)

  pay = df.values.tolist()

  while len(pay) >= 1:
    if len(pay) >= 5:
      wallet.transfer(pay[-1][0], pay[-1][1], pay[-1][2], pay[-1][3])
      wallet.transfer(pay[-2][0], pay[-2][1], pay[-2][2], pay[-2][3])
      wallet.transfer(pay[-3][0], pay[-3][1], pay[-3][2], pay[-3][3])
      wallet.transfer(pay[-4][0], pay[-4][1], pay[-4][2], pay[-4][3])
      wallet.transfer(pay[-5][0], pay[-5][1], pay[-5][2], pay[-5][3])
      print(pay[-1], pay[-2], pay[-3], pay[-4], pay[-5])
      del pay[-5:]
    else:
      wallet.transfer(pay[-1][0], pay[-1][1], pay[-1][2], pay[-1][3])
      print(pay[-1])
      del pay[-1]
    sleep(5)

  print("Payout complete.")

if __name__ == "__main__":
    
    unlockWallet()
    checkHiveWallet()
    payout()
    