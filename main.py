import random
import copy
import numpy as np
import redis
import math
import json

"""
颜色用 a、b、c来表示
位置用0，1，2，3来表示

"""
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class Bottle:
    """
    例如：data=[a,b,c,d]
    """
    FIRST_SCORE = 8
    SECOND_SCORE = 4
    THIRD_SCORE = 2
    FORTH_SCORE = 1

    def __init__(self, data):
        self.size = 4
        self.container = data
        self.success = False

    def __str__(self):
        return str(self.container)

    def length(self):
        return len(self.container)

    def getOut(self, count=0):
        # 可以拿出来的情况
        outType = ""
        subContainer = []
        num = len(self.container)
        deep = num
        i = 0
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
            i += 1
            if i == count:
                break
        return subContainer

    def takeItIn(self, subContainer):
        # 可以放进来的情况
        self.container.extend(subContainer)

    def checkSuccess(self):
        # 校验瓶子是否已经是满格同色
        if self.length() != self.size:
            self.success = False
            return False
        topOne = ""
        for item in self.container:
            if topOne == "":
                topOne = item
            if item != topOne:
                self.success = False
                return False
        self.success = True
        return True

    # 计算得分
    def computeScore(self):
        colorList = self.container
        if len(colorList) == 0:
            return 0
        if len(colorList) == 1:
            return Bottle.FIRST_SCORE
        if len(colorList) == 2:
            if colorList[0] == colorList[1]:
                return (Bottle.FIRST_SCORE + Bottle.SECOND_SCORE) * 2
            else:
                return Bottle.FIRST_SCORE + Bottle.SECOND_SCORE

        if len(colorList) == 3:
            if colorList[0] == colorList[1] == colorList[2]:
                return (Bottle.FIRST_SCORE + Bottle.SECOND_SCORE + Bottle.THIRD_SCORE) * 3
            elif colorList[0] == colorList[1]:
                return (Bottle.FIRST_SCORE + Bottle.SECOND_SCORE) * 2 + Bottle.THIRD_SCORE
            elif colorList[1] == colorList[2]:
                return Bottle.FIRST_SCORE + (Bottle.SECOND_SCORE + Bottle.THIRD_SCORE) * 2
            else:
                return Bottle.FIRST_SCORE + Bottle.SECOND_SCORE + Bottle.THIRD_SCORE

        if len(colorList) == 4:
            if colorList[0] == colorList[1] == colorList[2] == colorList[3]:
                return (Bottle.FIRST_SCORE + Bottle.SECOND_SCORE + Bottle.THIRD_SCORE + Bottle.FORTH_SCORE) * 4
            # 三个相同
            elif colorList[0] == colorList[1] == colorList[2]:
                return (Bottle.FIRST_SCORE + Bottle.SECOND_SCORE + Bottle.THIRD_SCORE) * 3 + Bottle.FORTH_SCORE
            elif colorList[1] == colorList[2] == colorList[3]:
                return Bottle.FIRST_SCORE + (Bottle.SECOND_SCORE + Bottle.THIRD_SCORE + Bottle.FORTH_SCORE) * 3
            # 两个相同
            elif colorList[0] == colorList[1]:
                return (Bottle.FIRST_SCORE + Bottle.SECOND_SCORE) * 2 + Bottle.THIRD_SCORE + Bottle.FORTH_SCORE
            elif colorList[1] == colorList[2]:
                return Bottle.FIRST_SCORE + (Bottle.SECOND_SCORE + Bottle.THIRD_SCORE) * 2 + Bottle.FORTH_SCORE
            elif colorList[2] == colorList[3]:
                return Bottle.FIRST_SCORE + Bottle.SECOND_SCORE + (Bottle.THIRD_SCORE + Bottle.FORTH_SCORE) * 2
            else:
                return Bottle.FIRST_SCORE + Bottle.SECOND_SCORE + Bottle.THIRD_SCORE + Bottle.FORTH_SCORE

    def isSameColor(self):
        if self.length() == 0:
            return True
        for item in self.container:
            if item != self.container[0]:
                return False
        return True


"""
先随机进行匹配，然后记录下来过程，这样多试试
等到后面进行匹配的时候先去查询一下过去成功的经验，有没有似曾相识的节点是这个状态，然后执行这个记录

每进行一次就记录下来当前所有的排列组合，然后进行计算

第一步，先实现随机游戏

第二步，实现穹举实现，然后记录下所有的步骤。
"""

"""
尝试倒
"""


def tryPour(bottleOut, bottleIn):
    """

    :param bottleOut: 尝试倒出去
    :param bottleIn:  尝试倒进来
    :return:
    """

    # 校验bottleIn是否已经

    # bottleOut 是否是空瓶
    if bottleOut.length() == 0:
        return False
    # bottleIn 是否是满瓶
    if bottleIn.length() == bottleIn.size:
        return False
    # 倒进去的瓶子是空的
    if bottleIn.length() == 0:
        outLength = bottleOut.length()
        subContainer = bottleOut.getOut()
        if len(subContainer) == outLength:
            bottleOut.takeItIn(subContainer)
            return False
        bottleIn.takeItIn(subContainer)
        return True
    # 颜色不一致  不可以
    if bottleOut.container[-1] != bottleIn.container[-1]:
        return False
    # =============可以倒进来一部分的情况
    # bottleIn
    lackCount = bottleIn.size - bottleIn.length()

    # subContainer = ["a","b"...]
    subContainer = bottleOut.getOut(lackCount)
    bottleIn.takeItIn(subContainer)
    return True


def isPourAble(bottleOut, bottleIn):
    # bottleOut 是否是空瓶
    if bottleOut.length() == 0:
        return False
    # bottleIn 是否是满瓶
    if bottleIn.length() == bottleIn.size:
        return False
    # 倒进去的瓶子是空的
    if bottleIn.length() == 0:
        if bottleOut.isSameColor():
            return False
        return True
    # 颜色不一致  不可以
    if bottleOut.container[-1] != bottleIn.container[-1]:
        return False

    return True


def playGame(bottleList=[]):
    if bottleList == []:
        bottle1 = Bottle(["a", "d", "b", "b"])
        bottle2 = Bottle(["a", "a", "b", "b"])
        bottle3 = Bottle(["c", "c", "d", "d"])
        bottle4 = Bottle(["d", "a", "c", "c"])
        bottle5 = Bottle([])
        bottle6 = Bottle([])
        bottleList = [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6]
    print("开始状态：")
    for x in bottleList:
        print("  ", x, end="")
    i = 0
    m = 0
    with open("train.txt", "a") as f:
        f.write("\n\n")
    recordData = {}
    parentName = ""
    while True:

        # 检查状态
        bottleList_left = []

        for item in bottleList:
            if not item.checkSuccess():
                bottleList_left.append(item)
        bottleList_left_deepcopy = copy.deepcopy(bottleList_left)

        if len(bottleList_left) == 2 and bottleList_left[0].length() == 0 and bottleList_left[1].length() == 0:
            break

        # 挑选出 倒出和倒入的瓶子
        # indexOut = random.randint(0, len(bottleList_left) - 1)
        indexList = random.sample(range(0, len(bottleList_left)), 2)
        outIndex = indexList[0]
        inIndex = indexList[1]

        bottleOut = bottleList_left[outIndex]
        # bottleList_left.pop(indexOut)
        # indexIn = random.randint(0, len(bottleList_left) - 1)
        bottleIn = bottleList_left[inIndex]
        # 判断是否可以到

        res = tryPour(bottleOut, bottleIn)
        print("outIndex==", outIndex, " inIndex==", inIndex)
        print([b.container for b in bottleList_left])
        print(res)
        if res:

            i += 1

            print(" ")
            print("已经执行：%d 步" % (i,))

            print("  ")
            print("===bottleList_left_print====")
            scoreList = []
            dataList = []
            for bott in bottleList_left_deepcopy:
                print(bott, end=" ")
                score = bott.computeScore()
                if score == 60:
                    continue
                scoreList.append(score)
                dataList.append(bott.container)

            std = math.ceil(np.std(scoreList) * 1000000)
            name = str(len(scoreList)) + "-" + str(std)

            if parentName != "":
                recordData[parentName]["sonName"] = name

            data = {}
            data["outIndex"] = outIndex
            data["inIndex"] = inIndex
            data["bottleList"] = [bottle.container for bottle in bottleList_left_deepcopy]
            r.hset(name, "outIndex", outIndex)
            r.hset(name, "inIndex", inIndex)
            recordData[name] = data
            parentName = name
            # with open("train.txt", "a") as f:
            #     f.write(str(np.std(scoreList)) + "  " + str(sum(scoreList)) + "   " + str(scoreList) + "   " + str(
            #         dataList) + "\n")
            # f.write(str(np.var(scoreList)) + "  " + str(sum(scoreList)) + "   " + str(scoreList) + "\n")

        m += 1
        if m == 100000:
            print(" ")
            print("死循环")
            recordData = {}
            break
    print(" ")
    print("游戏结束")
    print("总执行步骤:", i)
    print("结果如下:")
    for x in bottleList:
        print("  ", x, end="")
    with open("train.txt", "a") as f:
        jsonData = json.dumps(recordData)
        f.write(jsonData)


if __name__ == '__main__':
    # bottle1 = Bottle(["a", "b", "c", "d"])
    # bottle2 = Bottle(["e", "d", "f", "a"])
    # bottle3 = Bottle(["a", "g", "b", "h"])
    # bottle4 = Bottle(["c", "h", "h", "e"])
    # bottle5 = Bottle(["g", "i", "i", "c"])
    # bottle6 = Bottle(["a", "h", "f", "b"])
    # bottle7 = Bottle(["b", "i", "d", "e"])
    # bottle8 = Bottle(["g", "f", "i", "f"])
    # bottle9 = Bottle(["c", "e", "g", "d"])
    # bottle10 = Bottle([])
    # bottle11 = Bottle([])
    # bottleList = [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6, bottle7, bottle8, bottle9, bottle10, bottle11]
    # playGame(bottleList)

    # bottle1 = Bottle(["a", "b", "c", "b"])
    # bottle2 = Bottle(["c", "e", "f", "a"])
    # bottle3 = Bottle(["g", "a", "c", "h"])
    # bottle4 = Bottle(["j", "g", "h", "i"])
    # bottle5 = Bottle(["c", "h", "i", "a"])
    # bottle6 = Bottle(["f", "i", "k", "f"])
    # bottle7 = Bottle(["d", "g", "k", "l"])
    #
    # bottle8 = Bottle(["d", "l", "l", "j"])
    # bottle9 = Bottle(["h", "l", "k", "e"])
    # bottle10 = Bottle(["e", "d", "d", "j"])
    # bottle11 = Bottle(["k", "j", "i", "g"])
    # bottle12 = Bottle(["f", "b", "b", "e"])
    # bottle13 = Bottle([])
    # bottle14 = Bottle([])
    #
    # bottleList = [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6, bottle7, bottle8, bottle9, bottle10, bottle11,
    #               bottle12, bottle13, bottle14]
    # playGame(bottleList)

    playGame()
