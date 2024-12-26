from data.data import data
from algorithms.abo_csp import ABO_CSP
import json


abo = ABO_CSP(data)

# print(json.dumps(abo.getBuffaloes(50), indent=2))
#! Obtener los búfalos aleatoriamente
buffs = abo.getBuffaloes(1)
abo._printTable(buffs)
#! búsqueda del mejor búfalo
print(json.dumps(abo.bgmaxSearch(buffs), indent=2))
