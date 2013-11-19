
class auctionGreedy:
    __playerId = 0
    __playersNum = 0
    __typesNum = 0
    __goal = 0
    __itemsList = None
    __itemsCount = None
    __bidAmount = 0
    __bidAmountRemainder = 0
    __itemIwant = -1
    __itemsIHave = 0

    def __initStrategy1(self):
        self.__bidAmount = 100 / self.__goal
        self.__bidAmountRemainder = 100 - (self.__goal * self.__bidAmount)
        #self.__stepsToWinEach()

    def __getStrategy1Str(self):
        if self.__itemsList[0] == self.__itemIwant:
            if self.__itemsIHave > 0:
                return str(self.__bidAmount)
            else:
                return str(self.__bidAmount + self.__bidAmountRemainder)
        else:
            return '0'
    
    def __init__(self, inputStr):
        self.__parseInputStr(inputStr)
        self.__initStrategy1()

    def getStrategyStr(self):
        return self.__getStrategy1Str()
    
    def __parseInputStr(self, str):
        # input format:
        # <player_id> <no_players> <no_types> <goal> <item_list>
        params = str.split(' ')
        self.__playerId = int(params[0])
        self.__playersNum = int(params[1])
        self.__typesNum = int(params[2])
        self.__goal = int(params[3])
        
        self.__itemsList = []
        self.__itemsCount = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for itemStr in params[4:]:
            item = int(itemStr)
            self.__itemsList.append(item)
            self.__itemsCount[item] = self.__itemsCount[item] + 1
            if self.__itemIwant == -1 and self.__itemsCount[item] == self.__goal:
                self.__itemIwant = item
                print 'Item I want is ' + itemStr
                
        #print self.__itemsCount

    def stepsToWinItem(self, itemNum, neededNum):
        found = 0
        for i in range(0, len(self.__itemsList)):
            if self.__itemsList[i] == itemNum:
                found += 1
                if neededNum == found:
                    return i

        return 100000

    def __stepsToWinEach(self):
        for key in self.__itemsCount.keys():
            stepsToWinTmp = self.stepsToWinItem(key, self.__goal)
            print 'Steps to win ' + str(self.__goal) + ' of ' + str(key) + ' are ' + str(stepsToWinTmp)
            if stepsToWinTmp < stepsToWin:
                stepsToWin = stepsToWinTmp
                self.__itemIwant = key
                print 'Item I want is ' + str(self.__itemIwant)

    def setAuctionResult(self, resStr):
        res = resStr.split(' ')
        if int(res[0]) == self.__playerId and self.__itemsList[0] == self.__itemIwant:
            self.__itemsIHave += 1
            
        del self.__itemsList[0]

        
if __name__ == '__main__':

    inputStr = '1 2 2 2 0 1 1 0 0 0 1 1 0 0 1 0 1 0 0 1 0 1 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 0 0 1 1 1 0 1 1 0 1 1 1 1 1 0 0'
    a = auctionGreedy(inputStr)
    bidStr = a.getStrategyStr()
    print 'bid amount = ' + bidStr
    a.setAuctionResult('0 10 ')
    bidStr = a.getStrategyStr()
    print 'bid amount = ' + bidStr
