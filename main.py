
import random


"""
颜色用 a、b、c来表示
位置用0，1，2，3来表示

"""


class Bottle():
    """
    例如：data=[a,b,c,d]
    """

    def __int__(self, data):
        self.size = 4
        self.container = data

    # def begin(self,dataList):
    #     self.container = dataList

    def length(self):
        return len(self.container)

    def getOut(self):
        # 可以拿出来的情况
        outType = ""
        subContainer = []
        num = len(self.container)
        deep = num
        while True:
            if deep == 0:
                break
            deep -= 1
            topOne = self.container.pop()
            if len(subContainer) == 0:
                outType = topOne
                subContainer.append(topOne)
            else:
                if topOne == outType:
                    subContainer.append(topOne)
                else:
                    self.container.append(topOne)
                    break

    def takeItIn(self, subContainer):
        # 可以放进来的情况
        self.container.extend(subContainer)

    def checkSuccess(self):
        if self.length() != self.size:
            return False
        else:
            item = ""
            for x in self.container:
                if item == "":
                    item = x
                if x != item:
                    return False
            return True


"""
先随机进行匹配，然后记录下来过程，这样多试试
等到后面进行匹配的时候先去查询一下过去成功的经验，有没有似曾相识的节点是这个状态，然后执行这个记录

每进行一次就记录下来当前所有的排列组合，然后进行计算

第一步，先实现随机游戏

第二步，实现穹举实现，然后记录下所有的步骤。
"""


def playGame(bottleList):
    bottle1 = Bottle(["a", "b", "c", "d"])
    bottle2 = Bottle(["a", "b", "c", "d"])
    bottle3 = Bottle(["a", "b", "c", "d"])
    bottle4 = Bottle(["a", "b", "c", "d"])
    bottle5 = Bottle()
    bottle6 = Bottle()
    bottleList = [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6]
    index = random.randint(0, len(bottleList) - 1)
    bottleList

if __name__ == '__main__':
    pass
