import pandas as pd
from hiveengine.api import Api
from hiveengine.tokenobject import Token
import time, datetime, json

# Instantiate Hive-Engine API
api = Api(url = "https://engine.rishipanthee.com/")

# Function to generate CSV file with Accounts / Amounts / Symbol (and Memo) from Datadf
def genCSV() :
	now = datetime.datetime.now()
	month = now.strftime("%b")
	day = now.strftime("%d")
	year = now.strftime("%y")
	fileName = payToken + "-" + month + day + year + ".csv"
	print("File name:", fileName)
	path = r"~/alivepay/pay/"
	try :
		df.to_csv(path+fileName, index = False)
		print("File successfully created: " + fileName)
	except :
		print("Can't create CSV file, please change your user rights in this folder: " + path)

# Remove project holders to just have the users holders
def removeHolders(dropHolders) :
    for holder in dropHolders:
        indexHolder = df[df["account"] == holder].index
        df.drop(indexHolder, inplace = True)
        print("Successfully removed: " + holder)

def getTokenPrecision(symbol) :
	tk = Token(symbol, api = api)
	tokenInfo = tk.get_info()
	decimalNmber = tokenInfo["precision"]
	return decimalNmber

#get list of all holders to remove them from payout
jsonfile = open('./config.json')
config = json.load(jsonfile)
jsonfile.close

payMemo = str("Daily payout based on your " + config['payoutToken'] + " stake.")

# Get list of all token holders
holders = api.find_all("tokens", "balances", query = {"symbol": config['payoutToken']})

deletedHolders = config["holders"]

## Generate CSV from each payout token
for payoutToken in config['tokens'] :
    payToken = payoutToken["symbol"]
    payAmount = payoutToken["amount"]
    minOwnedStake = payoutToken["minOwnedStake"]

    # Generate Datadf (from Pandas lib)
    df = pd.DataFrame(holders)

    df.drop(columns = ["_id", "balance", "pendingUnstake", "delegationsIn"], inplace = True)

    # Remove holders from getHolders JSON file
    removeHolders(deletedHolders)

    df["pendingUndelegations"] = df["pendingUndelegations"].astype(float)
    df["stake"] = df["stake"].astype(float)
    df["delegationsOut"] = df["delegationsOut"].astype(float)

    df = df.assign(ownedStake = df.sum(axis = 1, numeric_only = True))

    decNum = getTokenPrecision(config['payoutToken'])
    df["ownedStake"] = df["ownedStake"].round(decNum)

    indexZero = df[df["ownedStake"] < minOwnedStake].index
    df.drop(indexZero, inplace = True)
    df.drop(columns = ["symbol", "stake", "delegationsOut", "pendingUndelegations"], inplace = True)

    df.sort_values(by=["ownedStake"], inplace = True, ascending = False)

    # Get decimal numbers from payout token
    payDec = getTokenPrecision(payToken)

    sumStake = float(df["ownedStake"].sum())

    df = df.assign(amount = (payAmount * (df.sum(axis = 1, numeric_only = True) / sumStake)))
    df["amount"] = df["amount"].astype(float)
    indexZero2 = df[df["amount"] < 0.00000001].index
    df.drop(indexZero2, inplace = True)
    df["amount"] = df["amount"].round(payDec)

    sumAmount = df["amount"].sum().round(payDec)
    print("Sum payout: " + sumAmount + payToken)
    df["amount"] = df["amount"].astype(str)

    df = df.assign(symbol = payToken)
    df = df.assign(memo = payMemo)

    df.drop(columns = ["ownedStake"], inplace = True)

    genCSV()

    del df

    print("Waiting 2 sec before next")
    time.sleep(2)
