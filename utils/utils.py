import random
import copy

def getRandomAvailableOrder(orders):
    result = None
    if sum(orders.values()) == 0:
        return result
    while True:
        randomOrder = random.choice(list(orders.keys()))
        newOrderValue = orders[randomOrder] - 1
        if newOrderValue >= 0:
            orders[randomOrder] -= 1
            result = randomOrder
            break
    return result


# def getAvailableRandomNumber(currents, maxNumber, minNumber=1):
#     result = None
#     while True:
#         randomNumber = random.randint(minNumber, maxNumber)
#         if randomNumber not in currents:
#             result = randomNumber
#             break
#     return result
