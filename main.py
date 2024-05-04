from data.data import data
from algorithms.abo_csp import ABO_CSP
import json


abo = ABO_CSP(data)

# print(json.dumps(abo.getBuffaloes(50), indent=2))
abo._printTable(abo.getBuffaloes(50))
