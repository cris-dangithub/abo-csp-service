import random
from utils.utils import getRandomAvailableOrder
from copy import deepcopy


class ABO_CSP:
    def __init__(self, data):
        self.items = data["steelSheet"]
        self.totalItemLengths = self._getTotalItemLengths()
        print({"totalItemLengths": self.totalItemLengths})
        # self.long_stock = long_stock
        # self.num_buffaloes = num_buffaloes
        # self.sol_population = sol_population
        # self.exploration_rate = exploration_rate
        # self.iterations = iterations
        # self.lp1 = lp1
        # self.lp2 = lp2

    def bgmaxSearch(self, buffaloes: list[dict]):
        """
        Best solution is the one with the least waste
        """
        bestBuffaloe = min(buffaloes, key=lambda x: x["percentage"])
        return {
            "buffNum": bestBuffaloe["buffNum"],
            "percentage": bestBuffaloe["percentage"],
            "cuttingPattern": bestBuffaloe["cuttingPattern"],
        }

    def _getMb(self, buffaloes: list[dict]):
        """
        Fitness function
        """
        for buff in buffaloes:
            buff["fitness"] = (
                buff["stocksWithWaste"] + buff["totalWaste"]["totalLength"]
            )
        return buffaloes

    def getBuffaloes(self, qbuff):
        """
        qbuff -> quanitity buffaloues to generate
        """
        assert qbuff > 0, "Quantity must be positive number"
        buffaloes = []
        for i in range(qbuff):
            buffaloes.append({"buffNum": i + 1, **self._createRandomBuffaloe()})
        return buffaloes

    def _getTotalItemLengths(self):
        return sum(
            [round(item["lengthBar"] * item["barsQuantity"], 2) for item in self.items]
        )

    def _createRandomBuffaloe(
        self,
    ):  # TODOCRIS Pasar a una clase "Buffaloe"
        individualItemsByNOrder = []
        totalIndividualItems = sum(item["barsQuantity"] for item in self.items)
        print({"totalIndividualItemsQuantity": totalIndividualItems})
        ordersByIdxQuantity = {
            idx: item["barsQuantity"] for idx, item in enumerate(self.items)
        }
        print({"ordersByIdxQuantity": ordersByIdxQuantity})
        # Obtener las posiciones randoms a ejecutar los patrones de corte
        ordersByIdxQuantityCopyToGetPositions = deepcopy(ordersByIdxQuantity)
        for i in range(totalIndividualItems):
            randomOrderIndex = getRandomAvailableOrder(
                orders=ordersByIdxQuantityCopyToGetPositions
            )
            individualItemsByNOrder.append(randomOrderIndex)
            print(
                ">>",
                {
                    "ordersByIdxQuantityCopyToGetPositions": ordersByIdxQuantityCopyToGetPositions,
                    "individualItemsByNOrder": individualItemsByNOrder,
                    "randomOrderIndex": randomOrderIndex,
                },
            )
        return self._getBuffaloeData(individualItemsByNOrder, ordersByIdxQuantity)

    def _getCuttingPattern(self, idxOrders):
        return ["#{}".format(self.items[idx]["n_order"]) for idx in idxOrders]

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
                totalWaste["totalLength"] = round(
                    totalWaste["totalLength"] + currentStockLength, 2
                )
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
            "stocksWithWaste": stocksWithWaste,
            "totalWaste": totalWaste,
            "percentage": self._getWastePercentage(totalWaste["totalLength"]),
            "cuttingPattern": self._getCuttingPattern(listIndividualOrders),
        }
        return result

    def _getWastePercentage(self, wasteTotalLength):
        return round((wasteTotalLength / self.totalItemLengths) * 100, 2)

    def _printTable(self, table: list[dict]):
        print("TABLA RESUMEN DE BUFALOS")
        print(
            "{:<10} {:<15} {:<10} {}".format(
                "Buffalo", "used/wtWast", "Waste (%)", "Info waste"
            )
        )
        for idx, obj in enumerate(table):

            print(
                "{:<10} {:<15} {:<10} {}".format(
                    obj["buffNum"],
                    "{}/{}".format(obj["stockUsed"], obj["stocksWithWaste"]),
                    "%{}".format(obj["percentage"]),
                    obj["totalWaste"],
                )
            )
        print("\n")
