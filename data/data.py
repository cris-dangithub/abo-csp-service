weights = {
    "#2": 0.25,
    "#3": 0.56,
    "#4": 0.994,
    "#5": 1.552,
    "#6": 2.235,
    "#7": 3.042,
    "#8": 3.973,
    "#9": 5.06,
    "#10": 6.404,
    "#11": 7.907,
    "#14": 11.38,
    "#18": 20.24,
}  # (NSR10 - kg/m)

data = {
    "steelSheet": [
        {"n_order": 1, "gauge": "#4", "lengthBar": 1.5, "barsQuantity": 7},
        {"n_order": 2, "gauge": "#4", "lengthBar": 4, "barsQuantity": 3},
        {"n_order": 6, "gauge": "#4", "lengthBar": 3.6, "barsQuantity": 5},
    ],
    "stock": [
        {"gauge": "#4", "lengthBar": 6, "barsQuantity": 20},
        {"gauge": "#4", "lengthBar": 9, "barsQuantity": 20},
        {"gauge": "#4", "lengthBar": 12, "barsQuantity": 20},
    ],
    "config": {},
}

for order in data["steelSheet"]:
    order["totalLength"] = round(order["lengthBar"] * order["barsQuantity"], 2)
    order["totalWeight"] = round(order["totalLength"] * weights[order["gauge"]], 2)
