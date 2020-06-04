from pathlib import Path
from .string import *
import os


path = os.path.abspath('.')

# Renews success.txt, failed.txt and tickets.txt logs
def cleanLogs(fileList):

    print(cleaningLogs())

    for textFile in fileList:
        my_file = Path(path + "/resources/" + textFile)
        if my_file.is_file():
            os.remove(my_file)
        with open(my_file,"w") as wf:
            wf.write("")


if __name__ == '__main__':
    fileList = ["success.txt/","failed.txt/","tickers.txt/"]
    cleanLogs(fileList)
