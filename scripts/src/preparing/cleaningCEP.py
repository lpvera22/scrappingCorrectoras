import pandas as pd

DATA_DIR = '../../data/'

cep = pd.read_csv(DATA_DIR + 'ceps.txt', sep="\t", header=None, names=["cep", "estado", "region", "extra"])
cep.to_csv(DATA_DIR + 'ceps.csv', index=False)

# cep = pd.read_excel(DATA_DIR + 'Lista_de_CEPs.xlsx')
# newCEP = cep[['Estado', 'Localidade', 'CEP Inicial']]
# newCEP.rename(columns={'CEP Inicial': 'CEP'}, inplace=True)
# print(newCEP)
