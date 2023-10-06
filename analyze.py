""""
Lê as bases limpas.
Salvas localmente como bases (formato pickle), após rodar read_organize_databases.py

Analisar os indicadores (README.md)

"""
import pickle

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}


def emissions_by_municipality(data):
    pass


if __name__ == '__main__':
    with open('bases', 'rb') as handler:
        b = pickle.load(handler)
