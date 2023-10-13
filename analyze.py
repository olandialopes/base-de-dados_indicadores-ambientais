""""
Lê as bases limpas.
Salvas localmente como bases (formato pickle), após rodar read_organize_databases.py

Analisar os indicadores (README.md)

"""
import pandas as pd
import os
import pickle

print("Diretório atual:", os.getcwd())

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}


def emissions_by_municipality(data):
    pass


def quant_efluentes_cnae(data):
    data['clas_cnae20'] = data['clas_cnae20'].str[:2]
    print(data.groupby(by='clas_cnae20').agg('mean')['quant_efluentes_liquidos'].sort_values(ascending=False).head(20))


if __name__ == '__main__':
    nome = 'bases_massa_desindentificada'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

# Concatenar todos os DataFrames em um único DataFrame
data = pd.concat(b.values(), ignore_index=True)

#-------------------------------------------------------------------------------------------
#  Agrupar os dados por 'ano' e 'class_cnae20' e somar a quantidade de efluentes líquidos
result1 = data.groupby(['ano', 'clas_cnae20'])['quant_efluentes_liquidos'].sum().reset_index()
result2 = data.groupby(['ano', 'clas_cnae20'])['quant_poluentes_emitidos'].sum().reset_index()
result3 = data.groupby(['ano', 'clas_cnae20'])['quant_residuos_solidos'].sum().reset_index()
result4 = data.groupby(['ano', 'clas_cnae20'])['quant_consumida_energia_acordo_tipo'].sum().reset_index()
result5 = data.groupby(['ano', 'clas_cnae20'])['quantidade_energia_padrao_calorias'].sum().reset_index()
result6 = data.groupby(['ano', 'clas_cnae20'])['co2_emissions'].sum().reset_index()

#Salvar o resultado em um arquivo CSV - SOMA
result1.to_csv('analise descritiva/result1-tabela_cnae_ano_soma_quant_efluentes_liquidos.csv', index=False)
result2.to_csv('analise descritiva/result2-tabela_cnae_ano_soma_quant_poluentes_emitidos.csv', index=False)
result3.to_csv('analise descritiva/result3-tabela_cnae_ano_soma_quant_residuos_solidos.csv', index=False)
result4.to_csv('analise descritiva/result4-tabela_cnae_ano_soma_quant_consumida_energia_acordo_tipo.csv', index=False)
result5.to_csv('analise descritiva/result5-tabela_cnae_ano_soma_quantidade_energia_padrao_calorias.csv', index=False)
result6.to_csv('analise descritiva/result6-tabela_cnae_ano_soma_co2_emissions.csv', index=False)
#-------------------------------------------------------------------------------------------
# Agrupar os dados por 'ano' e 'class_cnae20' e média da quantidade de efluentes líquidos - MÉDIA
result1 = data.groupby(['ano', 'clas_cnae20'])['quant_efluentes_liquidos'].mean().reset_index()
result2 = data.groupby(['ano', 'clas_cnae20'])['quant_poluentes_emitidos'].mean().reset_index()
result3 = data.groupby(['ano', 'clas_cnae20'])['quant_residuos_solidos'].mean().reset_index()
result4 = data.groupby(['ano', 'clas_cnae20'])['quant_consumida_energia_acordo_tipo'].mean().reset_index()
result5 = data.groupby(['ano', 'clas_cnae20'])['quantidade_energia_padrao_calorias'].mean().reset_index()
result6 = data.groupby(['ano', 'clas_cnae20'])['co2_emissions'].mean().reset_index()
#Salvar o resultado em um arquivo CSV - MÉDIA
result1.to_csv('analise descritiva/2-result1-tabela_cnae_ano_media_quant_efluentes_liquidos.csv', index=False)
result2.to_csv('analise descritiva/2-result2-tabela_cnae_ano_media_quant_poluentes_emitidos.csv', index=False)
result3.to_csv('analise descritiva/2-result3-tabela_cnae_ano_media_quant_residuos_solidos.csv', index=False)
result4.to_csv('analise descritiva/2-result4-tabela_cnae_ano_media_quant_consumida_energia_acordo_tipo.csv', index=False)
result5.to_csv('analise descritiva/2-result5-tabela_cnae_ano_media_quantidade_energia_padrao_calorias.csv', index=False)
result6.to_csv('analise descritiva/2-result6-tabela_cnae_ano_media_co2_emissions.csv', index=False)
#-------------------------------------------------------------------------------------------
# Agrupar os dados por 'ano', 'estado' e 'class_cnae20' e média da quantidade de efluentes líquidos
result1 = data.groupby(['ano', 'estado', 'clas_cnae20'])['quant_efluentes_liquidos'].mean().reset_index()
result2 = data.groupby(['ano', 'estado', 'clas_cnae20'])['quant_poluentes_emitidos'].mean().reset_index()
result3 = data.groupby(['ano', 'estado', 'clas_cnae20'])['quant_residuos_solidos'].mean().reset_index()
result4 = data.groupby(['ano', 'estado', 'clas_cnae20'])['quant_consumida_energia_acordo_tipo'].mean().reset_index()
result5 = data.groupby(['ano', 'estado', 'clas_cnae20'])['quantidade_energia_padrao_calorias'].mean().reset_index()
result6 = data.groupby(['ano', 'estado', 'clas_cnae20'])['co2_emissions'].mean().reset_index()
#Salvar o resultado em um arquivo CSV -MÉDIA
result1.to_csv('analise descritiva/3-tabela_cnae_ano_estado_media_quant_efluentes_liquidos.csv', index=False)
result2.to_csv('analise descritiva/3-tabela_cnae_ano_estado_media_quant_poluentes_emitidos.csv', index=False)
result3.to_csv('analise descritiva/3-tabela_cnae_ano_estado_media_quant_residuos_solidos.csv', index=False)
result4.to_csv('analise descritiva/3-tabela_cnae_ano_estado_media_quant_consumida_energia_acordo_tipo.csv', index=False)
result5.to_csv('analise descritiva/3-tabela_cnae_ano_estado_media_quantidade_energia_padrao_calorias.csv', index=False)
result6.to_csv('analise descritiva/3-tabela_cnae_ano_estado_media_co2_emissions.csv', index=False)
#-------------------------------------------------------------------------------------------
# Agrupar os dados por 'ano', 'estado', 'municipio' e 'class_cnae20' e média da quantidade de efluentes líquidos
result1 = data.groupby(['ano', 'estado', 'mun', 'clas_cnae20'])['quant_efluentes_liquidos'].mean().reset_index()
result2 = data.groupby(['ano', 'estado', 'mun', 'clas_cnae20'])['quant_poluentes_emitidos'].mean().reset_index()
result3 = data.groupby(['ano', 'estado', 'mun', 'clas_cnae20'])['quant_residuos_solidos'].mean().reset_index()
result4 = data.groupby(['ano', 'estado', 'mun', 'clas_cnae20'])['quant_consumida_energia_acordo_tipo'].mean().reset_index()
result5 = data.groupby(['ano', 'estado', 'mun', 'clas_cnae20'])['quantidade_energia_padrao_calorias'].mean().reset_index()
result6 = data.groupby(['ano', 'estado', 'mun', 'clas_cnae20'])['co2_emissions'].mean().reset_index()
#Salvar o resultado em um arquivo CSV
result1.to_csv('analise descritiva/4-tabela_cnae_ano_municipio_media_quant_efluentes_liquidos.csv', index=False)
result2.to_csv('analise descritiva/4-tabela_cnae_ano_municipio_media_quant_poluentes_emitidos.csv', index=False)
result3.to_csv('analise descritiva/4-tabela_cnae_ano_municipio_media_quant_residuos_solidos.csv', index=False)
result4.to_csv('analise descritiva/4-tabela_cnae_ano_municipio_media_quant_consumida_energia_acordo_tipo.csv', index=False)
result5.to_csv('analise descritiva/4-tabela_cnae_ano_municipio_media_quant_efluentes_liquidos.csv', index=False)
result6.to_csv('analise descritiva/4-tabela_cnae_ano_municipio_media_quantidade_energia_padrao_calorias.csv', index=False)
#-------------------------------------------------------------------------------------------
data = pd.concat(b.values(), ignore_index=True)
#eficiencia do tratamento abaixo de 80% significa que não está atendendo a legislação
# Filtrar os dados onde 'perc_efficiency_treatment' é menor ou igual a 80% e diferente de zero
filtered_data = data[(data['perc_efficiency_treatment'] <= 80) & (data['perc_efficiency_treatment'] != '0')]

filtered_data_sort = filtered_data.sort_values(by = 'clas_cnae20' , ascending=True)

# Criar um novo DataFrame com as colunas desejadas
filtered_data_subset = filtered_data[['clas_cnae20', 'perc_efficiency_treatment']]
#Salvar o resultado em um arquivo CSV
filtered_data_subset.to_csv('analise descritiva/5-tabela_cnae_abaixo80eficienc_efluentes_liquidos.csv', index=False)

# Contar a quantidade de ocorrências de cada valor na coluna 'clas_cnae20'
count_by_cnae20 = filtered_data['clas_cnae20'].value_counts().reset_index()

# Renomear as colunas - cnae e número de ocorrências de não conformidade (abaixo de 80#)
count_by_cnae20.columns = ['class_cnae20', 'qtde']

#imprimir o número de ocorrências
print(count_by_cnae20)

#Salvar o resultado em um arquivo CSV - número de ocorrência de não conformidade (abaixo de 80%)
count_by_cnae20.to_csv('analise descritiva/6-tabela_cnae_ocorrencia_abaixo80eficienc_efluentes_liquidos.csv', index=False)




