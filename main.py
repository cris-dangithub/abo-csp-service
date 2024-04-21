from data.data import data
from algorithms.abo_csp import ABO_CSP


abo = ABO_CSP(data)

print(abo.getBuffaloes(5))
