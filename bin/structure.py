import sys
from pathlib import Path
from .string import *
from .dir import *
from scrape import *
from csv import reader
from time import sleep
import pandas
import csv
import os
import pickle
import numpy

path = os.path.abspath('.')

class Company:

    def __init__(self,ticker,period):

        # Initialize Company

        self.ticker,self.period = ticker,period
        self.metaData,self.currencies = [0,0,0],[None,None,None]
        self.path = os.path.join(path,"companyData",period,ticker)
        self.paths = self.getFinancialsPath()
        self.incomeStatement,self.balanceSheet,self.cashFlowStatement = self.getFinancialStatements()
        self.metrics = self.getMetrics()
        self.dates = self.getDates()
        self.yahooData = {}

        # Yahoo Statistics
        # # TODO:  This should also all be done with a method

        """ This should be in preserve
        parameter = "marketCap"
        parameterFileName = parameter + ".csv"

        with open(os.path.join(path,"resources",parameterFileName)) as f:
            csv_reader = csv.reader(csv_file, delimiter=',')
            parameterTickers,parameterValues = [],[]
            for row in csv_reader:
                tickers.append(row[0]),tickers.append(row[1])
            parameterPacket = []


        if self.ticker in parameterTickers:
            self.yahooStatistics.append((parameter,))
            """

    # Initialization Methods
    def getFinancialsPath(self):
        return {"bs":os.path.join(self.path,"bs","data.csv"),
                "is":os.path.join(self.path,"is","data.csv"),
                "cf":os.path.join(self.path,"cf","data.csv")}

    def getDates(self):
        dates,isDates,bsDates,cfDates = [],[],[],[]
        if self.metaData == [1,1,1]:
            isDates = self.incomeStatement.index.tolist()
            bsDates = self.balanceSheet.index.tolist()
            cfDates =self.balanceSheet.index.tolist()
        if "TTM" in isDates:
            isDates.remove("TTM")
        if "TTM" in bsDates:
            bsDates.remove("TTM")
        if "TTM" in cfDates:
            cfDates.remove("TTM")
        return [isDates,bsDates,cfDates]

    def getFinancialStatements(self):

        incomeStatement,balanceSheet,cashFlowStatement = None,None,None

        # Income Statement
        if is_non_zero_file(self.paths["is"]):

            with open(self.paths["is"],'r') as f:
                # df Data
                incomeStatement = pandas.read_csv(f,skiprows=1,index_col=0).T
                incomeStatement.columns = incomeStatement.columns.str.lower()


            with open(self.paths["is"],'r') as f:
                # currency data
                rawCurrency = list(csv.reader(f,delimiter=','))[1][0]
                self.currencies[0] = rawCurrency.split()[5]

            self.metaData[0] = 1

        else:
            incomeStatement = None

        # Balance Sheet
        if is_non_zero_file(self.paths["bs"]):

            # df Data
            with open(self.paths["bs"],'r') as f:
                balanceSheet = pandas.read_csv(f,skiprows=1,index_col=0).T
                balanceSheet.columns = balanceSheet.columns.str.lower()
            self.metaData[1] = 1

            # currency data
            with open(self.paths["bs"],'r') as f:
                rawCurrency = list(csv.reader(f,delimiter=','))[1][0]
                self.currencies[1] = rawCurrency.split()[5]

        else:
            balanceSheet = None

        # Cash Flow Statement
        if is_non_zero_file(self.paths["cf"]):

            # df Data
            with open(self.paths["cf"],'r') as f:
                cashFlowStatement = pandas.read_csv(f,skiprows=1,index_col=0).T
                cashFlowStatement.columns = cashFlowStatement.columns.str.lower()
            self.metaData[2] = 1

            # currency data
            with open(self.paths["cf"],'r') as f:
                rawCurrency = list(csv.reader(f,delimiter=','))[1][0]
                self.currencies[2] = rawCurrency.split()[5]


        else:
            cashFlowStatement = None

        return incomeStatement,balanceSheet,cashFlowStatement

    def getMetrics(self):

        if self.metaData == [1,1,1]:
            isMetrics = self.incomeStatement.T.index.tolist()
            bsMetrics = self.balanceSheet.T.index.tolist()
            cfMetrics = self.cashFlowStatement.T.index.tolist()
        else:
            isMetrics,bsMetrics,cfMetrics = [],[],[]

        return [isMetrics,bsMetrics,cfMetrics]


    # Accessor Methods
    def peek(self):
        print("-"*130+"\n* ticker: " + str(self.ticker))
        print("\n* Income Statement: ")
        print(self.incomeStatement.T)
        print("\n* Balance Sheet")
        print(self.balanceSheet.T)
        print("\n* Cash Flow Statement: ")
        print(self.cashFlowStatement.T)
        print("\n* Income Statement Metrics")
        print(self.metrics[0])
        print("\n* Balance Sheet Metrics")
        print(self.metrics[1])
        print("\n* Cash Flow Metrics")
        print(self.metrics[2])

    def has(self,sheet,metric):

        if sheet == "is":
            if metric in self.metrics[0]:
                return True
            else:
                return False
        elif sheet == "bs":
            if metric in self.metrics[1]:
                return True
            else:
                return False
        elif sheet == "cf":
            if metric in self.metrics[2]:
                return True
            else:
                return False
        else:
            print("INVALID HAS")
            quit()

    def get(self,sheet,date,item):

        if sheet == "is":
            getValue = self.incomeStatement.T
        elif sheet == "bs":
            getValue = self.balanceSheet.T
        elif sheet == "cf":
            getValue = self.cashFlowStatement.T
        else:
            print("Sheet DNE")

        getValue = getValue.at[item,date]
        getValue = getValue[~numpy.isnan(getValue)]

        if getValue.size == 0:
            getValue = float(0)
        else:
            getValue = float(getValue[0])
        return getValue

    def printCompany(self):
        print(str(self.metaData) + " - " + str(self.ticker))

class Universe:

    def __init__(self,period):

        # TODO:  Similarly This should all be done with methods

        print("-"*130)
        print(" "*60+"U N I V E R S E\n")
        print("\r* Initializing Universe...",end="")
        self.path = os.path.join(path,"companyData",period)
        print("\r* Path:" + str(self.path))

        #print(readingData()), sleep(1)
        self.companies,self.removed,self.tickers = [],[],os.listdir(self.path)
        readingCounter,readingMax = 0,len(self.tickers)
        for ticker in self.tickers:
            self.companies.append(Company(ticker,period))
            readingCounter+=1
            print(str("\r* Packaging Companies-- ")+str(round(100*readingCounter/(readingMax+0.01),2))+"%",end="")
        self.tickers = self.getTickers()

        if ".DS_Store" in self.tickers:
            self.tickers.remove(".DS_Store")
        print("* Number of Companies: " + str(len(self.tickers)))
        print("\n")
        #print(finishData())
        counter = 0
        for company in self.companies:
            counter += company.metaData[0]+company.metaData[1]+company.metaData[2]
            self.percent = 100 * float(counter)/float((len(self.tickers)+0.01)*3)
        #print(successfulReads(percent)), sleep(1)
        self.scrub()

        # Download and Attach Yahoo Data to Companies
        # Market Cap
        self.attachYahooData(['marketCap'])

        self.downloadCurrencyData()

        self.getMetrics()
        self.statistics()
        print("-"*130)

    # We need to Super hyper turbocharge this baby. Maybe we can create some kind of highway Dict?
    def getCompany(self,ticker):
        for company in self.companies:
            if ticker == company.ticker:
                return company

    def get(self,ticker,sheet,date,item,currency):
        # Get Company
        sheetNumber = getSheetNumber(sheet)
        company = self.getCompany(ticker)
        sheetCurrency = company.currencies[sheetNumber]
        itemValue = company.get(sheet,date,item)
        return self.convertCurrency(sheetCurrency,currency,itemValue)

    def getTickers(self):
        tickers = []
        for company in self.companies:
            tickers.append(company.ticker)
        return tickers

    def add(self,tickers):

        exceptionCount,exceptionMax = 0,len(tickers)

        for ticker in tickers:
            try:
                if company.ticker not in self.tickers:
                    self.companies.append(company)
                    self.tickers.append(company.ticker)
                print()
            except Exception as e:
                exceptionCount+=1
                pass

        if len(tickers) >= 100:
            print("Success Percent: " + str(round(float(100*(exceptionMax-exceptionCount)/exceptionMax),2)))
            print("Exceptions Percent: " + str(round(float(100*exceptionCount/exceptionMax),2)))

        self.tickers = self.getTickers()

    def remove(self,company):

        if company.ticker in self.tickers:
            self.companies.remove(company)
            self.removed.append(company)
            self.tickers.remove(company.ticker)


    def feasibilityTransformation(self):
        print("="*130+"\nFEASIBILITY TRANSFORMATION\n"+"="*130)
        invalidCompanies,bias = list(),0
        transformationCounter,transformationMax = 0,len(self.companies)

        for indx in range(len(self.companies)):
            print(str("\r* Transforming Companies Percent Complete -- ")+str(round(100*transformationCounter/transformationMax,2))+"%",end="")
            if sum(self.companies[indx+bias].metaData) != 3:
                invalidCompanies.append(self.companies[indx+bias])
                del self.companies[indx+bias]
                del self.tickers[indx+bias]
                bias-=1

        print("- " + str(len(invalidCompanies)) + " Companies Found and Deleted...")
        self.tickers = self.getTickers()
        return(len(invalidCompanies))

    def attachYahooData(self,parameters):
        # Download Yahoo Data
        #scrape.runYahooScraper(self.tickers,parameter)
        # Attach Yahoo Data
        for parameter in parameters:
            tickerParameterDict,tickersNotDownloaded = {},[]
            fileName = "./companyData/" + parameter + ".csv"

            # Check if File Exists g
            if not os.path.exists(fileName):
                with open(fileName,"w") as f:
                    print(fileName + " Created!")

            with open(fileName) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    tickerParameterDict[row[0]] = row[1]

            for company in self.companies:
                if company.ticker not in tickerParameterDict.keys():
                    tickersNotDownloaded.append(company.ticker)

            print("Yahoo Data Already Downloaded: " + str(len(tickerParameterDict.keys())))
            print("Yahoo Data Not Already Downloaded: " + str(len(tickersNotDownloaded)))

            runYahooScraper(tickersNotDownloaded,parameter)

            tickerParameterDict = {}

            with open(fileName) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    tickerParameterDict[row[0]] = row[1]

            for company in self.companies:
                try:
                    company.yahooData[parameter] = tickerParameterDict[company.ticker]
                except Exception as e:
                    print("Could not attach Yahoo Data: " + company.ticker)
                    pass

            self.dumpUniverse(os.path.abspath('.'),self.companies[0].period)


    def downloadCurrencyData(self):
        fileName,currencySet = "./companyData/currency.csv",set()
        tickerParameterDict,tickersNotDownloaded = {},[]

        for company in self.companies:
            isCur,bsCur,cfCur = [company.currencies[i] for i in range(3)]
            currencySet.add(isCur),currencySet.add(bsCur),currencySet.add(cfCur)

        currencyTickerList = list(currencySet)
        currencyTickerList = [currencyTickerList[i] + "USD=X" for i in range(len(currencyTickerList)) ]

        if not os.path.exists(fileName):
            with open(fileName,"w") as f:
                print(fileName + " Created!")

        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                tickerParameterDict[row[0]] = row[1]

        for currencyTicker in currencyTickerList:
            if currencyTicker not in tickerParameterDict.keys():
                tickersNotDownloaded.append(currencyTicker)

        print("Yahoo Data Already Downloaded: " + str(len(tickerParameterDict.keys())))
        print("Yahoo Data Not Already Downloaded: " + str(len(tickersNotDownloaded)))

        runYahooScraper(tickersNotDownloaded,"currency")

        tickerParameterDict = {}

        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                tickerParameterDict[row[0]] = row[1]

    def dumpUniverse(self,path,period):
        print(preservingAndDumping())
        #self.feasibilityTransformation()
        with open(os.path.join(path,"companyData",period + "store.pckl"), 'wb') as df:
            pickle.dump(self, df)
        print("="*130 + "\nDONE\n"+"="*130)

    def peek(self):

        print(universeSummary())
        print(successful())
        [company.printCompany() for company in self.companies]

        print(incomplete())
        for company in self.removed:
            if sum(company.metaData) != 0 and sum(company.metaData) != 3:
                company.printCompany()

        print(failed())
        [company.printCompany() for company in self.removed]


    def convertCurrency(self,fromCur,toCur,value):
        #Currency Conversion
        fileName = "./companyData/currency.csv"
        currencyDict = {}

        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                currencyDict[row[0]] = row[1]

        currencyKey = fromCur + toCur + "=X"
        conversionFactor = float(currencyDict[currencyKey])

        #print("CONVERSION: from: " + fromCur + " -> to " + toCur +" => " + str(value) + " - " + str(conversionFactor * value))
        return conversionFactor * value

    def size(self):
        counter = 0
        for company in self.companies:
            counter += 1
        return counter

    def clean(self):

        print("="*130+"\nCLEANING UNIVERSE\n"+"="*130)

        cleanCount = 0

        isCleaner = ["The proxy server could not handle the request","<!*********** error message start **************>","</head><body>"]
        isCleaner += ["Proxy Error</title>"]
        bsCleaner = ["</body></html>","<h1>Proxy Error</h1>","The proxy server could not handle the request"]
        cfCleaner = ["The proxy server could not handle the request","Error reading","<title>502 Proxy Error</title>"]

        cleanMax,removeCount,cleanCount = len(self.companies),0,0

        for company in self.companies:
            for metric in company.metrics:
                for sheetCleaner in [isCleaner,bsCleaner,cfCleaner]:
                    for cleaner in sheetCleaner:
                        if cleaner in metric:
                            self.remove(company)
                            removeCount+=1

            print(str("\r* Cleaning Companies Percent Complete -- ")+str(round(100*cleanCount/cleanMax,2))+"%",end="")
            cleanCount += 1

        print("- " + str(removeCount) + " Companies Found and Deleted...")
        print("\nUNIVERSE CLEANED\n")

        self.tickers = self.getTickers()
        return(int(removeCount))


    def scrub(self):

        print("@"*130)
        print("SCRUB")

        cleanRemoveCount = self.clean()
        while cleanRemoveCount >= 10:
            cleanRemoveCount = self.clean()

        feasRemoveCount = self.feasibilityTransformation()
        while feasRemoveCount >= 10:
            feasRemoveCount = self.feasibilityTransformation()

        print("@"*130)


    def getMetrics(self):
        isMetrics,bsMetrics,cfMetrics = [],[],[]

        for company in self.companies:
            if sum(company.metaData) == 3:
                isMetrics = isMetrics + company.incomeStatement.T.index.tolist()
                bsMetrics = bsMetrics + company.balanceSheet.T.index.tolist()
                cfMetrics = cfMetrics + company.cashFlowStatement.T.index.tolist()

            isMetrics,bsMetrics,cfMetrics = list(set(isMetrics)),list(set(bsMetrics)),list(set(cfMetrics))

        self.metrics = [isMetrics,bsMetrics,cfMetrics]


    def statistics(self, verbose = None):

        numRemoved,numSuccess,numRedeemable,metrics,dataOut = 0,0,0,self.metrics,[]

        print("="*130+"\nUNIVERSE STATISTICS\n"+"="*130)
        print("- Universe Directory Path: " + str(self.path))
        print("- Company Count: " + str(len(self.companies)))
        print("- Ticker Count:" + str(len(self.tickers)))
        print("- Removed Count: " + str(len(self.removed)))
        print("- Metric Count: is-" + str(len(metrics[0])) + ", bs-" + str(len(metrics[1])) + ", cf-" + str(len(metrics[2])))

        for company in self.companies:
            if sum(company.metaData)==1 or sum(company.metaData) == 2:
                numRedeemable+=1

        print("- Redeemable Count: " + str(numRedeemable))

        print("- Meta Data Symbols")

        metaSymbolTemplate = [0,1]

        metaSymbols = [[sym_1,sym_2,sym_3] for sym_1 in metaSymbolTemplate for sym_2 in metaSymbolTemplate for sym_3 in metaSymbolTemplate]

        for metaSymbol in metaSymbols:
            metaSymbolCount = 0
            for company in self.companies:
                if company.metaData == metaSymbol:
                    metaSymbolCount+=1
            print(" "+str(metaSymbol) + " - " + str(metaSymbolCount))

        if True:
            fileList,percentages = ["top2000marketcap","NASDAQ","NYSE","MOTLEY"],[]

            for file in fileList:
                tickers = generateTickers([file])
                lenTickers,count = len(tickers), 0
                for ticker in tickers:
                    if ticker in self.tickers:
                        count += 1

                percentages.append(float(100*count/lenTickers))
                print(" - "+str(file) +": "+ str(float(100*count/lenTickers)))

def preserveUniverse(period):
    relativePath = os.path.abspath('.')
    universe = Universe(period)
    universe.dumpUniverse(relativePath,period)
    return universe

def loadUniverse(path,period):
    print(loadingUniverse())
    with open(os.path.join(path,"companyData",period+"store.pckl"),'rb') as rd:
        universe = pickle.load(rd)

        print()
        print("-"*130)
        print(" "*60+"U N I V E R S E\n")
        print("* Initializing Universe, standby...")
        print("* Path:" + str(universe.path))
        print("* Number of Companies: " + str(len(universe.tickers)))
        print("* Total Database Generated: " + str(universe.percent))

        print("-"*130)


        return universe


def getSheetNumber(sheet):
    if sheet == "is":
        return 0
    elif sheet == "bs":
        return 1
    elif sheet == "cf":
        return 2
    else:
        print("INVALID SHEET NUMBER ---- QUITTING")
        quit()

def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False


if __name__ == '__main__':
    print("*?")
