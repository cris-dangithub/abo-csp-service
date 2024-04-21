import random
from utils.utils import getRandomAvailableOrder
from copy import deepcopy


class ABO_CSP:
    def __init__(self, data):
        self.items = data["steelSheet"]
        # self.long_stock = long_stock
        # self.num_buffaloes = num_buffaloes
        # self.sol_population = sol_population
        # self.exploration_rate = exploration_rate
        # self.iterations = iterations
        # self.lp1 = lp1
        # self.lp2 = lp2

    def getBuffaloes(self, qbuff):
        """
        qbuff -> quanitity buffaloues to generate
        """
        if qbuff <= 0:
            raise ("Quantity must be positive number")
        buffaloes = []
        for i in range(qbuff):
            buffaloes.append(self._createRandomBuffaloe())
        return buffaloes

    def _createRandomBuffaloe(
        self,
    ):  # TODOCRIS Posiblemente pasar a una entidad "Buffaloe"
        individualItemsByNOrder = []
        totalIndividualItems = sum(item["barsQuantity"] for item in self.items)
        ordersByIdxQuantity = {
            idx: item["barsQuantity"] for idx, item in enumerate(self.items)
        }
        # Obtener las posiciones randoms a ejecutar los patrones de corte
        ordersByIdxQuantityCopyTOGetPositions = deepcopy(ordersByIdxQuantity)
        for i in range(totalIndividualItems):
            randomOrderIndex = getRandomAvailableOrder(
                orders=ordersByIdxQuantityCopyTOGetPositions
            )
            individualItemsByNOrder.append(randomOrderIndex)

        return self._getBuffaloeData(individualItemsByNOrder, ordersByIdxQuantity)

    def _getBuffaloeData(self, listIndividualOrders, ordersByQuantity):
        # Aplicar el stock (Ej: 6metros, 9metros, 12metros)#TODOCRIS Aplicar la clase Cutter
        stock = 6  # TODOCRIS Lo haremos con 6 de momento para probar, el problema principal será hacerlo con las demás longitudes, pues el algoritmo del trabajo de referencia solamente usa una longitud de stock
        stockUsed = 0
        stocksWithWaste = 0  # barras desperdiciadas
        totalWaste = {
            "totalLength": 0,
            "lenghts": [],
        }
        currentStockLength = stock

        print(ordersByQuantity)

        # Hacer los cortes en la demanda con el stock teniendo en cuenta los patrones de corte aleatorios generados
        for idx, idxSteelSheetOrder in enumerate(listIndividualOrders):
            cuttingResultInCurrentStock = round(
                currentStockLength - self.items[idxSteelSheetOrder]["lengthBar"], 2
            )
            # Evaluar el cortado en el stock actual
            if cuttingResultInCurrentStock > 0:
                # Si el corte no cabe en el stock actual, se procede a cortar en un nuevo stock
                currentStockLength = cuttingResultInCurrentStock
            elif cuttingResultInCurrentStock < 0:
                # Si el corte cabe en el stock actual, se procede a cortar en el stock actual, actualizando la longitud actual del stock actual
                totalWaste["totalLength"] = round(totalWaste["totalLength"] + currentStockLength, 2)
                totalWaste["lenghts"].append(currentStockLength)
                # usar un nuevo stock (generamos desperdicio)
                stocksWithWaste += 1
                stockUsed += 1
                currentStockLength = stock
            else:
                # cuando es cero, combinación de ambas condiciones anteriores
                stockUsed += 1
                currentStockLength = stock
            # Reducimos a 1 la cantidad de demanda actual
            ordersByQuantity[idxSteelSheetOrder] -= 1

        result = {
            "stockUsed": stockUsed,
            "ordersByQuantity": ordersByQuantity,
            "stocksWithWaste": stocksWithWaste,
            "totalWaste": totalWaste,
        }
        return result
