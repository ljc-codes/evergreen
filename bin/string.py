

borderCount = 130

# TODO: This FILE_NAME and all dependencies need to be changed.

# control.py

def currentFunctionality():
    text = "===================== Enchirideon Command Line Usage =====================\n\nrun:\'Python3 control.py [-c] [-u]\'\n\n[-c]   : [clean] = Purges Company Data Files and Log Files\n"
    text += "       : [cleanLogs] = Purges Company Log Files\n       : [cleanDirs] = Purges Company Data Files\n       : [makeDirs] = Creates Company Directories\n"
    text += "       : [easy] = [clean] + [makeDirs]\n       : [launch] = [clean] + [makeDirs] + [scrape]\n       : [scrape] = Scrape Morningstar for Company Data\n       : [preserve] [period] = Save Company Data Files (Downloaded) into Universe Object. Period is from Periodlist\n\n[-u]   : [-t] = Test"
    text += "\n===================== Enchirideon Command Line Usage =====================\n\n..\n."
    return text

def testing():
    return "*"*borderCount+"\n"+" "*round((borderCount-35)/2)+"~~--\__ T E S T I N G   M O D E __/--~~ \n"+"*"*borderCount

def morningstarInitialized():
    return "="*borderCount+"\nMORNINGSTAR SCRAPER INITIALIZED\n"+"="*borderCount

def morningstarFailed():
    return "="*borderCount+"\nMORNINGSTAR SCRAPER FAILED\n"+"="*borderCount


def quit(E):
    return "="*borderCount + str(E) +" -- QUITTING -- " + "="*borderCount


def cmdInput(argvInput):
    COMMANDLINE_INPUT = "Python3 "
    for arg in argvInput:
        COMMANDLINE_INPUT += (str(arg) +" ")
    return "\nCOMMANDLINE INPUT: " + COMMANDLINE_INPUT + "\n"


# structure.py

def readingData():
    return "*"*borderCount+"\nREADING DATA\n"+"*"*borderCount

def finishData():
    return "*"*borderCount+"\nFINISHED READING DATA"

def successfulReads(percent):
    return "\nSuccessful Reads: "+str(percent)+"% of total data\n"+"*"*borderCount

def preservingAndDumping():
    return "*"*borderCount + "\nPRESERVING AND DUMPING UNIVERSE...\n"+"*"*borderCount

def universeSummary():
    return "*"*borderCount + "\nUNIVERSE SUMMARY\n"+"*"*borderCount

def successful():
    return "\nSUCCESSFUL:\n "

def failed():
    return "\nFAILED:\n"

def incomplete():
    return "\nIMCOMPLETE:\n"

def loadingUniverse():
    return "-"*borderCount+"\nLOADING UNIVERSE...\n"


# dir.py

def dirsCreated():
    return "="*borderCount+"\n DIRS:company directories created \n"+"="*borderCount

def dirsUpdated():
    return "="*borderCount+"\n DIRS: company directories updated\n"+"="*borderCount

def dirsPurged():
    return "="*borderCount+"\n DIRS: company directories purged\n"+"="*borderCount

def loadingTickers():
    return "="*borderCount+"\n LOADING TICKERS \n"+"="*borderCount

def getting(file):
    return "\n     -> Getting: "+file+" \n"

def totalTickers(size):
    return "total tickers: "+str(size)+"\n"


#scrape.py

def failedPull(pull):
    return str(" * Failed Pulls: "+str(len(pull)) + " --- ("+str(round(len(pull)/3,1)) + " companies)")

def successfulPull(pull):
    return str(" * Successful Pulls: "+str(len(pull)) + "--- ("+str(round(len(pull)/3,1)) + " companies)")

def connectionEstablished():
    return "="*borderCount+"\n MORNINGSTAR CONNECTION ESTABLISHED \n"+"="*borderCount

def connectionKilled():
    return "="*borderCount+"\n MORNINGSTAR CONNECTION KILLED \n"+"="*borderCount

def torGetS(basicInfo,sizeInfo,attemptInfo,percentInfo):
    return "TOR GET : >>  Data Package: (R)  ||| (" + basicInfo +" ||| Data Size: " + sizeInfo + "|| Attempt: " + attemptInfo + " ||| Done: " + percentInfo +"%"

def torGetF(basicInfo,sizeInfo,attemptInfo,percentInfo):
    return "TOR GET : >>  Data Package: ( )  ||| (" + basicInfo +" ||| Data Size: " + sizeInfo + "|| Attempt: " + attemptInfo + " ||| Done: " + percentInfo +"%"

def yahooGetS(basicInfo,percentInfo):
    return "YAHOO FINANCIALS API : >>  Data Package: (R)  ||| " + basicInfo +" ||| Done: " + percentInfo +"%"

def yahooGetF(basicInfo,percentInfo):
    return "YAHOO FINANCIALS API : >>  Data Package: ( )  ||| " + basicInfo +" ||| Done: " + percentInfo +"%"

def torZero():
    return "-"*borderCount+"\nTOR GET : >>  0 Data size package detected... Changing ip address... hang on...\n" + "-" *borderCount

def dbStatus(percent):
    return "="*borderCount+"\n DATABASE GENERATED: "+percent+"\n"+"="*borderCount


#logs.py


def cleaningLogs():
    return "="*borderCount + "\n CLEANING LOGS: success.txt, failed.txt and tickers.txt logs purged \n" + "="*borderCount












# MISC


#Scrape.py

""""
DELTA 1: ~ PRESERVE FOR REFERENCE
ELIMINATED REDUNDANCY:
IMPORT FROM BIN

# Generates Tickers
def generateTickers(fileList):

    tickersRaw,tickerPacket = [],[]

    for file in fileList:

        if file == globalPath + "/resources/top2000marketcap.txt" or file == globalPath + "/resources/test.txt":
            tickersRaw = []

            with open(globalPath + "/resources/top2000marketcap.txt","r") as fi:
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

        elif file == "NASDAQ" or file == "NYSE":

            # Download NASDAQ or NYSE sheets

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


    # Gets Unique tickers
    return list(set(tickerPacket))


"""

# Structure.py

# Let's just directly get from the df. I think this might be faster than any other solution

"""    def getUniverseMetrics(self):
        isMetrics,bsMetrics,cfMetrics = [],[],[]
        for company in self.companies:

            for key,value in company.financialDicts[0].items():
                if 'Fiscal' not in key[0]:
                    isMetrics.append(key[0])

            for key,value in company.financialDicts[1].items():
                if 'Fiscal' not in key[0]:
                    bsMetrics.append(key[0])

            for key,value in company.financialDicts[2].items():
                if 'Fiscal' not in key[0]:
                    cfMetrics.append(key[0])

        return [list(set(isMetrics)),list(set(bsMetrics)),list(set(cfMetrics))]
"""

# Let's just stick to dfs.
""""

    def generateFinancialsDicts(self):

        print(self.ticker)
        isDict,bsDict,cfDict, = {},{},{}
        masterStatements = [self.incomeStatement[1:],self.balanceSheet[1:],self.cashFlowStatement[1:]]
        isDateList,bsDateList,cfDateList = self.incomeStatement[1][1:7],self.balanceSheet[1][1:7],self.cashFlowStatement[1][1:7]


        print(masterStatements[0])
        print(isDateList)

        for index in range(len(isDateList)):
            for row in masterStatements[0]:
                key = (str(row[0]),isDateList[index])
                isDict[key] = row[index]

        for index in range(len(bsDateList)):
            for row in masterStatements[1]:
                key = (str(row[0]),bsDateList[index])
                bsDict[key] = row[index]

        for index in range(len(cfDateList)):
            for row in masterStatements[2]:
                key = (str(row[0]),cfDateList[index])
                cfDict[key] = row[index]

        return [isDict,bsDict,cfDict]
"""
