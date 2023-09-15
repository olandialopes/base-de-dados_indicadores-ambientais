import pandas as pd

data = pd.read_csv('1-relatorio efluentes liquidos_ibama.csv', delimiter=';')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ da base original: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios da base original: {contagem_valores_municipios}')

# Colunas a serem excluidas
colunas_indesejadas = [
    'Código da Categoria', 'Código do Detalhe', 'Desc. Monitoramento Utilizado',
    'Compart. Ambiental da Emissão', 'Tipo de Emissão', 'Tipo Corpo Receptor',
    'Classe do Corpo Receptor', 'Nome do Corpo Hídrico', 'Corpo Receptor',
    'Qual?', 'Empresa Receptora do Efluente', 'Tipo de Emissão Para o Solo',
    '(Se outro) Qual?', 'Situação Cadastral','Latitude','Longitude',
    'Tipo de Tratamento', 'Nível de Tratamento', 'Detalhe'
]
#Escluir as colunas indesejadas, cujos nomes estão acima
data = data.drop(columns=colunas_indesejadas, axis=1)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ depois de excluir qualquer celula em branco: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios depois de excluir qualquer celula em branco:: {contagem_valores_municipios}')

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ depois de excluir qualquer celula valor igual a zero: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios depois de excluir qualquer celula valor igual a zero: {contagem_valores_municipios}')

# Contar valores únicos na coluna muncípio (quantidade de municípios na base de dados)
contagem_valores_unicos = data['Município'].nunique()

# Salvar as alterações de volta no arquivo CSV
data.to_csv('1-result_efluentes liquidos.csv', index=False)

