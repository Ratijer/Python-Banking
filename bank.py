# Created by Rachel Atijera on 5/30/18 
# These classes are all part of a bank system 

#Note1: [0] represents the Person class. [1] represents the Funds class.
#Note2: True = Transaction was successful.

from account import StorageOfAccounts
from account import Funds
from account import Person
from queue import Queue

#TODO: CREATE OUTPUT FILE AND WRITE INTO IT

#Set of actions that can be stored in a queue
class Transaction:
    def __init__(self, line = ""):
        self.__line = line 
        self.__transaction = line.split()[0]
        
    def doTransaction(self, storage, func = None):
            line = self.__line
            #Open new account
            if self.__transaction == "O":
                firstName = line.split()[2]
                lastName = line.split()[1]
                accountID = int(line.split()[3])
                transactionSuccess = self.openAccount(storage, accountID, firstName, lastName)                               
            #Deposit funds 
            elif self.__transaction == "D": 
                accountID = int(line.split()[1]) // 10
                fund = int(line.split()[1]) % 10
                money = int(line.split()[2])
                transactionSuccess = self.depositFunds(storage, accountID, fund, money)
                #Add to transaction history
                if transactionSuccess == True:
                    storage[accountID][1].recordTransaction(fund, line.strip())
            #Withdraw funds 
            elif self.__transaction == "W": 
                accountID = int(line.split()[1]) // 10
                fund = int(line.split()[1]) % 10
                fundAmount = storage[accountID][1].retrieveFund(fund)
                money = int(line.split()[2])
                transactionSuccess = self.withdrawFunds(storage, accountID, fund, money)

                #Add to transaction history
                #TODO: PUT THIS IN WITHDRAW METHOD 
                if transactionSuccess != True:
                    storage[accountID][1].recordTransaction(fund, line.strip() + " (Failed)")
                elif storage[accountID][1].retrieveFund(fund) < money:            
                    storage[accountID][1].recordTransaction(fund, "W " + str(accountID) + str(fund) + " " + str(fundAmount))
                else:
                    storage[accountID][1].recordTransaction(fund, line.strip())
            #Transfer funds  
            elif self.__transaction == "T":
                accountID1 = int(line.split()[1]) // 10            
                fund1 = int(line.split()[1]) % 10
                accountID2 = int(line.split()[3]) // 10           
                fund2 = int(line.split()[3]) % 10
                money = int(line.split()[2])                              
                transactionSuccess = self.transferFunds(storage, accountID1, accountID2, fund1, fund2, money)

                #Add to transaction history
                account1 = storage[accountID1]
                account2 = storage[accountID2]
                if transactionSuccess != True:                   
                    if account1 != None:
                        account1[1].recordTransaction(fund1, line.strip() + " (Failed)")
                    if account2 != None:
                        account2[1].recordTransaction(fund2, line.strip() + " (Failed)")
                else:
                    account1[1].recordTransaction(fund1, line.strip())
                    account2[1].recordTransaction(fund2, line.strip())   
            #Print history
            elif self.__transaction == "H":
                accountID = int(line.split()[1])
                transactionSuccess = self.printHistory(storage, accountID, func)
               
            #Print transaction error if there are any 
            if transactionSuccess != True:
                print(transactionSuccess)
                if func != None:
                    func(transactionSuccess + "\n")

    def getTransaction(self):
        return self.__transaction

    def getLine(self):
        return self.__line

    def setTransaction(self, transaction):
        self.__transaction = transaction

    def setLine(self, line):
        self.__line = line 

    def openAccount(self, storage, accountID, firstName = "", lastName = ""):
        client = Person(firstName, lastName)
        f = Funds()
        #Check to see if account doesn't already exist 
        if storage[accountID] != None: 
            return "ERROR: Account " +  str(accountID) + " is already open. Transaction refused."
        elif len(str(accountID)) != 4:
            return "ERROR: Account " + str(accountID) + " does not have four digits. Transaction refused."         
        else:
            storage.put(int(accountID), client, f) 
            return True 

    def depositFunds(self, storage, accountID, fundNum, money):
        if storage[accountID] == None:
            return "ERROR: Account " + str(accountID) + " not found. Transaction refused."
        else:
            storage[accountID][1].addToFund(fundNum, money)
            return True 

    def withdrawFunds(self, storage, accountID, fundNum, money):
        if storage.get(accountID) == None:
            return "ERROR: Account " + str(accountID) + " not found. Transaction refused."
        account = storage[accountID]
        #When there is not enough funds 
        if account[1].retrieveFund(fundNum) < money and fundNum != 0 and fundNum != 1 and fundNum != 2 and fundNum != 3:
            return "ERROR: Not enough funds to withdraw " + str(money) + " from " + account[0].getName() + " " + account[1].retrieveFundName(fundNum)
        #Insufficient funds in Market or Bond 
        elif account[1].retrieveFund(fundNum) < money and (fundNum == 0 or fundNum == 2):
            neededFunds = money - account[1].retrieveFund(fundNum)
            if account[1].retrieveFund(fundNum + 1) < neededFunds:
                #Record transaction in fund 
                account[1].recordTransaction(fundNum + 1, "W " + str(accountID) + str(fundNum + 1) + " " + str(neededFunds) + " (Failed)")
                return "ERROR: Not enough funds to withdraw " + str(money) + " from " + account[0].getName() + " " + account[1].retrieveFundName(fundNum) + " or " + account[0].getName() + " " + account[1].retrieveFundName(fundNum + 1)
            else:
                #Remove from other market/ bond 
                account[1].subtractFromFund(fundNum + 1, neededFunds)
                #Add to money market/ long-term bond
                account[1].addToFund(fundNum, neededFunds)
                account[1].subtractFromFund(fundNum, money)

                #Record transaction in fund 
                account[1].recordTransaction(fundNum + 1, "W " + str(accountID) + str(fundNum + 1) + " " + str(neededFunds))
                return True 
        elif account[1].retrieveFund(fundNum) < money and (fundNum == 1 or fundNum == 3):
            neededFunds = money - account[1].retrieveFund(fundNum)
            if account[1].retrieveFund(fundNum - 1) < neededFunds:             
                #Record transaction in fund 
                account[1].recordTransaction(fundNum - 1, "W " + str(accountID) + str(fundNum - 1) + " " + str(neededFunds) + " (Failed)")
                return "ERROR: Not enough funds to withdraw " + str(money) + " from " + account[0].getName() + " " + account[1].retrieveFundName(fundNum) + " or " + account[0].getName() + " " + account[1].retrieveFundName(fundNum - 1)
            else:
                #Remove from other market/ bond 
                account[1].subtractFromFund(fundNum - 1, neededFunds)
                #Add to primary money market/ short-term bond
                account[1].addToFund(fundNum, neededFunds)
                account[1].subtractFromFund(fundNum, money)

                #Record transaction in fund 
                account[1].recordTransaction(fundNum - 1, "W " + str(accountID) + str(fundNum - 1) + " " + str(neededFunds))
                return True 
        else:
            account[1].subtractFromFund(fundNum, money)
            return True 

    #Transfer from account1 to account2 
    def transferFunds(self, storage, accountID1, accountID2, fundNum1, fundNum2, money):
        if storage[accountID1] == None:
            return "ERROR: Account " + str(accountID1) + " not found. Transferal refused."
        if storage[accountID2] == None:
            return "ERROR: Account " + str(accountID2) + " not found. Transferal refused."        
        withdrawalSuccess = self.withdrawFunds(storage, accountID1, fundNum1, money)
        if withdrawalSuccess == True:
            storage[accountID2][1].addToFund(fundNum2, money)
            return True 
        else:
            account1 = storage[accountID1]
            account2 = storage[accountID2]
            return "ERROR: Not enough funds to transfer from " + account1[0].getName() + " " + account1[1].retrieveFundName(fundNum1) + " to " + account2[0].getName() + " " + account1[1].retrieveFundName(fundNum2)
    
    #Print transaction history 
    def printHistory(self, storage, accountID, func = None): 
        if len(str(accountID)) == 5:
            account = accountID // 10
        else:
            account = accountID
        if storage.get(account) == None:
            return "ERROR: Account " + str(accountID) + " not found. Transaction refused."
        if len(str(accountID)) == 4:
            accountID = int(accountID)
            account = storage[accountID]
            transactPerFund = account[1].retrieveTransactions()
            print("Transaction History for", account[0].getName(), "by fund.")
            if func != None:
                func("Transaction History for " + account[0].getName() + " by fund.\n")
            for fund in range(len(transactPerFund)):
                if len(transactPerFund[fund]) <= 0:
                    pass
                else:
                    result = ""
                    if fund == 0:
                        result = "Money Market: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 1:
                        result = "Prime Money Market: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 2:
                        result = "Long-Term Bond: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 3:
                        result = "Short-Term Bond: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 4:
                        result = "500 Index Fund: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 5:
                        result = "Capital Value Fund: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 6:
                        result = "Growth Equity Fund: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 7:
                        result = "Growth Index Fund: " + "$" + str(account[1].retrieveFund(fund))
                    elif fund == 8:
                         result = "Value Fund: " + "$" + str(account[1].retrieveFund(fund))
                    else: #fund == 9:
                         result = "Value Stock Index: " + "$" + str(account[1].retrieveFund(fund))
                    print(result)
                    if func != None:
                        func(result + "\n")

                    #Print transactions from fund
                    for transact in range(len(transactPerFund[fund])):
                        print(" ", transactPerFund[fund][transact])
                        if func != None:
                            func("  " + transactPerFund[fund][transact] + "\n")
        elif len(str(accountID)) == 5:
            accountID = int(accountID)
            account = storage[accountID // 10]
            fundAmount = account[1].retrieveFund(accountID % 10)
            fund = accountID % 10
            print("Transaction History for", account[0].getName(), account[1].retrieveFundName(fund) + ":", "$" + str(fundAmount))
            if func != None:
                func("Transaction History for " + account[0].getName() + " " + account[1].retrieveFundName(fund) + ": " + "$" + str(fundAmount) + "\n")
            transactPerFund = account[1].retrieveTransactions()
            #Print transactions from fund           
            for transact in range(len(transactPerFund[fund])):
                print(" ", transactPerFund[fund][transact])
                if func != None:
                    func("  " + transactPerFund[fund][transact] + "\n")
        return True

#Stores Acounts into SoA (BST), stores Transactions into queue, reads file, executes Transactions 
class Bank:     
    def __init__(self):
        self.__q = Queue()

    def __transactionsToQueue(self, text):
        file = open(text, "r")
        fileLen = sum(1 for line in open(text))
        for i in range(fileLen):
            t = Transaction(file.readline())
            self.__q.put(t)
        file.close()
     
    #Do a transactions, store accounts in BST storage, go through queue and deplete it 
    def executeTransactions(self, file, fileOutput):
        fileOutput = open(fileOutput, "w")
        self.__transactionsToQueue(file)
        storage = StorageOfAccounts()
        while self.__q.empty() == False:     
            t = self.__q.get()
            t.doTransaction(storage, fileOutput.write)
        
        #For console
        print("\nProcessing Done. Final Balances")
        storage.inOrderTraversal(print)

        #For output file 
        fileOutput.write("\nProcessing Done. Final Balances\n")
        storage.inOrderTraversal(fileOutput.write)

        fileOutput.close()