import json

class Used_Proxy():
    name = ""
    isBlocked = False
    isPaused = False
    qtyOfUsage = 0
    blockedAt = -1

    def __init__(self,name,isBlocked,qtyOfUsage):
        self.name = name
        self.isBlocked = isBlocked
        self.qtyOfUsage = qtyOfUsage

    def incUsage(self):
        self.qtyOfUsage+=1

    def createJson(self):
        json_dict = {
            "name":self.name,
            "isBlocked":self.isBlocked,
            "isPaused":self.isPaused,
            "qtyOfUsage":self.qtyOfUsage,
            "blockedAt":self.blockedAt,
        }

        return json.dumps(json_dict)


    def is_full_blocked(self):
        if (self.isPaused == True) and (self.isPaused == True):
            return True
        else:
            return False