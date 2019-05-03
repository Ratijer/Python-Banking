# Created by Rachel Atijera on 5/30/18 
# These classes are all part of a bank system 

#Node for StorageOfAccounts (BST). accountID is the key, person and funds are values 
class Account:
    def __init__(self, accountID, person = None, funds = None):
        self.__accountID = accountID
        self.__person = person
        self.__funds = funds 
        self.__leftChild = None
        self.__rightChild = None

    def getLeftChild(self):
        return self.__leftChild

    def getRightChild(self):
        return self.__rightChild

    def setLeftChild(self, theAccount):
        self.__leftChild = theAccount

    def setRightChild(self, theAccount):
        self.__rightChild = theAccount

    def getPerson(self):
        return self.__person

    def getFunds(self):
        return self.__funds

    def setPerson(self, person):
        self.__person = person

    def setFunds(self, funds):
        self.__funds = funds

    def getAccountID(self):
        return self.__accountID

    def setAccountID(self, accountID):
        self.__accountID = accountID

    def __repr__(self):
        return str(self.getPerson().getName()) + " Account ID: " + str(self.getAccountID())

    def __str__(self):
        return str(self.getPerson().getName()) + " Account ID: " + str(self.getAccountID())

    def isLeaf(self):
        return self.getLeftChild() == None and self.getRightChild() == None

#Values for Accounts
class Person:        
    def __init__(self, firstName = "", lastName = ""):
        self.__firstName = firstName
        self.__lastName = lastName

    def getFirst(self):
        return self.__firstName

    def getLast(self):
        return self.__lastName

    def getName(self):
        return self.__firstName + " " + self.__lastName 

    def setFirst(self, first):
        self.__firstName = first

    def setLast(self, last):
        self.__lastName = last

    def setName(self, first, last):
        self.__firstName = first
        self.__lastName = last

class Funds:          
    def __init__(self):
        self.__funds = [0] * 10
        #Money Market = funds[0]        #Prime Money Market = funds[1]    
	    #Long-Term Bond = funds[2]      #Short-Term Bond = funds[3]	     
	    #500 Index Fund = funds[4]      #Capital Value Fund = funds[5]    
	    #Growth Equity Fund = funds[6]  #Growth Index Fund = funds[7]	    
	    #Value Fund = funds[8]          #Value Stock Index = funds[9]

        #Transactions for each fund
        #Each fund will record transactions 
        self.__transactPerFund = [[], [], [], [], [], [], [], [], [], []]
           
    #Use this to print funds and their amount 
    def fundDictionary(self):
        fundDic = {"Money Market:": " $" + str(self.__funds[0]), "Prime Money Market:": " $" + str(self.__funds[1]), "Long-Term Bond:": " $" + str(self.__funds[2]), "Short-Term Bond:": " $" + str(self.__funds[3]), "500 Index Fund:": " $" + str(self.__funds[4]), 
                   "Capital Value Fund:": " $" + str(self.__funds[5]), "Growth Equity Fund:": " $" + str(self.__funds[6]), "Growth Index Fund:": " $" + str(self.__funds[7]), "Value Fund:": " $" + str(self.__funds[8]), "Value Stock Index:": " $" + str(self.__funds[9])}
        return fundDic

    #Record transaction from a single fund
    def recordTransaction(self, fundNum, transaction):
        self.__transactPerFund[fundNum].append(transaction)

    #Retrieve transactions from a single fund
    def retrieveTransactions(self):
        return self.__transactPerFund

    def retrieveFundName(self, fundNum):
        if fundNum == 0:
            return "Money Market"
        elif fundNum == 1:
            return "Prime Money Market"
        elif fundNum == 2:
            return "Long-Term Bond"
        elif fundNum == 3:
            return "Short-Term Bond"
        elif fundNum == 4:
            return "500 Index Fund"
        elif fundNum == 5:
            return "Capital Value Fund"
        elif fundNum == 6:
            return "Growth Equity Fund"
        elif fundNum == 7:
            return "Growth Index Fund"
        elif fundNum == 8:
            return "Value Fund"
        elif fundNum == 9:
            return "Value Stock Index"

    def getFunds(self):
        return self.__funds

    def setFunds(self, funds):
        self.__funds = funds

    #fundNum represent fund (0-9)
    def retrieveFund(self, fundNum):
        return self.__funds[fundNum]

    def addToFund(self, fundNum, money):
        self.__funds[fundNum] += money

    def subtractFromFund(self, fundNum, money):
        self.__funds[fundNum] -= money

#BST of Accounts   
class StorageOfAccounts:
    def __init__(self):
        self.__root = None
        self.__size = 0

    def getCount(self):
        return self.__size

    def isEmpty(self):
        return self.__size == 0

    def get(self, accountID):
        currentAccount = self.__root
        while currentAccount != None:
            if currentAccount.getAccountID() == accountID:
                return currentAccount.getPerson(), currentAccount.getFunds()
            elif currentAccount.getAccountID() > accountID:
                currentAccount = currentAccount.getLeftChild()
            else:
                currentAccount = currentAccount.getRightChild()
        return None
    
    def __getitem__(self, accountID):
        return self.get(accountID)

    def put(self, accountID, person, funds):
        if self.isEmpty():
            self.__root = Account(accountID, person, funds)
            self.__size += 1
            return
        currentAccount = self.__root
        while currentAccount != None:
            if currentAccount.getAccountID() == accountID:
                currentAccount.setPerson(person)
                currentAccount.setFunds(funds)
                return
            elif currentAccount.getAccountID() > accountID:
                if currentAccount.getLeftChild() == None:
                    newAccount = Account(accountID, person, funds)
                    currentAccount.setLeftChild(newAccount)
                    break
                else:
                    currentAccount = currentAccount.getLeftChild()
            else:
                if currentAccount.getRightChild() == None:
                    newAccount = Account(accountID, person, funds)
                    currentAccount.setRightChild(newAccount)
                    break
                else:
                    currentAccount = currentAccount.getRightChild()
        self.__size += 1

    def __setitem__(self, accountID, person, funds):
        self.put(accountID, person, funds)

    #Remove
    def remove(self, accountID):
        if self.__root == None:
            return None
        if self.__root.getAccountID() == accountID:
            self.__size -= 1
            if self.__root.getLeftChild() == None:
                self.__root = self.__root.getRightChild()
            elif self.__root.getRightChild() == None:
                self.root = self.__root.getLeftChild()
            else:
                replaceAccount = self.__getAndRemoveRightSmall(self.__root)
                self.__root.setaccountID(replaceAccount.getAccountID())
                self.__root.setPerson(replaceAccount.getPerson())
                self.__root.setFunds(replaceAccount.getFunds())
        else:
            currentAccount = self.__root
            while currentAccount != None:
                if currentAccount.getLeftChild() and currentAccount.getLeftChild().getAccountID() == accountID:
                    foundAccount = currentAccount.getLeftChild()
                    if foundAccount.isLeaf():
                        currentAccount.setLeftChild(None)
                    elif foundAccount.getLeftChild() == None:
                        currentAccount.setLeftChild(foundAccount.getRightChild())
                    elif foundAccount.getRightChild() == None:
                        currentAccount.setLeftChild(foundAccount.getLeftChild())
                    else:
                        replaceAccount = self.__getAndRemoveRightSmall(foundAccount)
                        foundAccount.setAccountID(replaceAccount.getAccountID())
                        foundAccount.setPerson(replaceAccount.getPerson())
                        foundAccount.setFunds(replaceAccount.getFunds())
                    break
                elif currentAccount.getRightChild() and currentAccount.getRightChild().getAccountID() == accountID:
                    foundAccount = currentAccount.getRightChild()
                    if foundAccount.isLeaf():
                        currentAccount.setRightChild(None)
                    elif foundAccount.getLeftChild() == None:
                        currentAccount.setRightChild(foundAccount.getRightChild())
                    elif foundAccount.getRightChild == None:
                        currentAccount.setRightChild(foundAccount.getLeftChild())
                    else:
                        replaceAccount = self.__getAndRemoveRightSmall(foundAccount)
                        foundAccount.setAccountID(replaceAccount.getAccountID())
                        foundAccount.setPerson(replaceAccount.getPerson())
                        foundAccount.setFunds(replaceAccount.getFunds())		            
                    break
                elif currentAccount.getAccountID() > accountID:
                    currentAccount = currentAccount.getLeftChild()
                else:
                    currentAccount = currentAccount.getRightChild()
            if currentAccount != None:
                self.__size -= 1

    #InOrder
    def inOrderTraversal(self, func):
        theAccount = self.__root
        self.__inOrderTraversalRec(self.__root, func)

    def __inOrderTraversalRec(self, theAccount, func):
        if theAccount != None:
            self.__inOrderTraversalRec(theAccount.getLeftChild(), func)
            if func == print:
                func(theAccount)
                fundDic = theAccount.getFunds().fundDictionary()
                for fund in fundDic:
                    func("   " + str(fund) + str(fundDic[fund]))
                func("")
            else:
                func("\n") 
                func(str(theAccount.getPerson().getName()) + " Account ID: " + str(theAccount.getAccountID()) + "\n")    
                fundDic = theAccount.getFunds().fundDictionary()
                for fund in fundDic:
                    func("    " + str(fund) + str(fundDic[fund]) + "\n")                                 
            self.__inOrderTraversalRec(theAccount.getRightChild(), func)