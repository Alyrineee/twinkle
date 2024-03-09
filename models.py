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
        self.name = 'star'
        self.__code = self.__generate()
        self.rank = random.choice(rare)
        self.date = None

    def check(self,num,index):
        if num == self.__code[index]:
            return True
        else:
            return False

class cat:
    def __init__(self,name):
        self.name = name
        self.stars = 0
        self.hungry = 50
    def eat(self):
        pass








