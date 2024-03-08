class star:
    def __generate(self):
        import random
        key = str()
        for i in range(16):
            bit = str(random.randint(0, 1))
            key += bit
        return key
    def __init__(self):
        self.name = 'star'
        self.__code = self.__generate()

    def check(self,num,index):
        if num == self.__code[index]:
            return True
        else:
            return False





