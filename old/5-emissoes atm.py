import pandas as pd

data = pd.read_csv('5-relatorio_emissoes atmosfericas ibama.csv', delimiter=';')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ da base original: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios da base original: {contagem_valores_municipios}')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Categoria de Atividade', 'Código do Detalhe', 'Detalhe', 'Observações',
    'Situação Cadastral', 'Densidade', 'Unidade de Medida - densidade', 'Justificativa para alteração da densidade',
    'Poder Calorífico Inferior', 'Unidade de Medida - Poder Calorífico Inferior',
    'Justificativa para alteração do Poder Calorífico Inferior',
    'Justificativa para Alteração do Conteúdo de Carbono', 'Fator de Oxidação',
    'Unidade de Medida - Fator de Oxidação',
    'Justificativa para Alteração do Fator de Oxidação', 'Conteúdo de Carbono',
    'Unidade de Medida - Conteúdo de Carbono'
]
# Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

valores_unicos_unidade = data['Unidade de Medida'].unique()

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
data.to_csv('5-result_emissoes_atm.csv', index=False)

print("Valores únicos da coluna 'Unidade de Medida':")
print(valores_unicos_unidade)