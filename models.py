import random


class star:
    def __generate(self):
        key = str()
        for i in range(8):
            bit = str(random.randint(0, 1))
            key += bit
        return key
    def __init__(self):
        rare = ['common','rare','epic','legendary']
        self.name = 'None'
        self.code = self.__generate()
        self.rank = random.choice(rare)
        self.date = None

    def check(self,num):
        pass

class cat:
    def __init__(self,name,id):
        self.name = name
        self.stars = 0
        self.hungry = 100
        self.id = id
    def eat(self):
        pass

class lot:
    def __generate(self):
        return 0
    def __init__(self,tg,code):
        self.id = self.__generate()
        self.tg = tg
        self.code = code
        self.winner = 'False'











