from torrequest import TorRequest
from csv import reader
from .string import *
import os
import shutil
import sys
import string


globalPath = os.path.abspath(__file__ + "/../../")

"""
GENERATE DIRECTORIES:
    Cleans directories and generates directories from
"""
def generateDirectories(globalPath,tickers,periodList,sheetList):
    path = globalPath + "/companyData/"
    for period in periodList:
        os.mkdir(path + period + "/")
        for company in tickers:
            os.mkdir(path + period + "/" + company)
            with open(globalPath + "/resources/tickers.txt","a") as log:
                log.write(company + "\n")
            for sheet in sheetList:
                os.mkdir(path+period+ "/" + company + "/" + sheet)
    print(dirsCreated())


"""UPDATE DIRECTORIES:
Updates Company Data in: "../companyData" from "../resources/tickers.txt"
"""
def updateDirectories(globalPath,tickers,periodList,sheetList):

    path = globalPath + "/companyData/"
    currentTickers = []
    with open(globalPath + "/resources/tickers.txt","r") as ip:
        currentTickers.append(ip.readlines())
    currentTickers = list(set([x[0:len(x)-1] for x in currentTickers[0]]))

    exclusionSet = set(tickers) - set(currentTickers)

    for period in periodList:
        for ticker in exclusionSet:
            if ticker not in currentTickers:
                try:
                    os.mkdir(path+period+ "/" + ticker)
                    for sheet in sheetList:
                        os.mkdir(path+period+ "/" + ticker+"/"+sheet)
                except Exception as e:
                    print(e)


    print(exclusionSet)



    """
    for period in periodList:
        for company in tickers:
            if (company in currentTickers) == False:
                os.mkdir(path + period + "/" + company)
                for sheet in sheetList:
                    os.mkdir(path+period+ "/" + company + "/" + sheet)

    print(dirsUpdated())
    """

"""
CLEAN DIRECTORIES:
Purges all Company Data in: "../companyData"
"""
def cleanDirectories(globalPath):

    path = globalPath + "/companyData/"
    folder = os.listdir(path)

    for item in folder:
        if item.isdigit():
            shutil.rmtree(path + item + "/")

    print(dirsPurged())



"""
CLEAN DIRECTORIES (HELPER METHOD):
Generates Tickers from fileList
"""
def generateTickers(fileList):

    tickersRaw,tickerPacket = [],[]

    print(loadingTickers())

    for file in fileList:

        print(getting(file))
        if file =="top2000marketcap" or file == "test":

            FILE_NAME = "/resources/"+file+".txt"
            tickersRaw = []

            with open(globalPath + FILE_NAME,"r") as fi:
                content = fi.readlines()

            for line in content:
                line = line.replace("/",".")
                if "$" in line:
                    tickersRaw.append(line)

            for line in tickersRaw:
                sentence = line.split()
                for i in range(len(sentence)-1):
                    if "$" in sentence[i+1]:
                        tickerPacket.append(sentence[i])

        # Download NASDAQ or NYSE sheets
        elif file == "NASDAQ" or file == "NYSE":
            url = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=*&render=download"
            tickerRaw = []
            FILE_NAME = file+".csv"

            with open(os.path.join(globalPath,"resources",FILE_NAME),'wb') as of:
                tr = TorRequest(password = 'sardonicDolphin')
                response = (tr.get(url.replace("*",file))).content
                of.write(response)

            with open(os.path.join(globalPath,"resources",FILE_NAME),'r') as ipf:
                csv_data = reader(ipf)
                [tickerRaw.append(x[0]) for x in list(csv_data)]

            tickerPacket = tickerPacket + tickerRaw

        # Download YAHOO WORLD SHEETS
        elif file == "YAHOOWORLD" or file == "MOTLEY":
            tickerRaw = []
            FILE_NAME = file+".csv"

            with open(os.path.join(globalPath,"resources",FILE_NAME),encoding="utf8", errors='ignore') as ipf:
                csv_data = reader(ipf)
                [tickerRaw.append(x[0]) for x in csv_data]

            tickerPacket = tickerPacket + tickerRaw

        elif file == "BRUTE":
            alphabet = str(string.ascii_uppercase[:]) + " "
            tickerRaw = [w+x+y for w in alphabet for x in alphabet for y in alphabet]
            tickerRaw = [x.strip(" ") for x in tickerRaw]
            tickerRaw = [x for x in tickerRaw if len(x) > 0]
            tickerPacket = tickerPacket + tickerRaw

    tickerPacket = list(set(tickerPacket))
    print(totalTickers(len(tickerPacket)))
    return tickerPacket


if __name__ == '__main__':

    fileList = ["top2000marketcap","NASDAQ","NYSE","MOTLEY","YAHOOWORLD"]
    baseUrl = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=*&reportType=^&period=_&dataType=A&order=asc&columnYear=5&number=3'
    gatherPath = "./shell/gather.sh"
    sheetList = ["is","cf","bs"]
    periodList = ["12"]
    logList = ["success.txt/","failed.txt/","tickers.txt/"]


    #updateDirectories(globalPath,tickers,periodList,sheetList)
    # Get Ticker Data
    #tickers = generateTickers(fileList)

    #cleanDirectories("/Users/LuigiCharles/Desktop/enchiridion")

    #generateDirectories("/Users/LuigiCharles/Desktop/enchiridion",tickers,periodList,sheetList)

    updateDirectories("/Users/LuigiCharles/Desktop/enchiridion",tickers,periodList,sheetList)
