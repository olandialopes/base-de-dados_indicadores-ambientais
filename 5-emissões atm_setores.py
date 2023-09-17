import pandas as pd

data = pd.read_csv('5-relatorio_emissoes atmosfericas ibama.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
'Código da Categoria','Código do Detalhe','Detalhe', 'Observações',
'Situação Cadastral', 'Densidade','Unidade de Medida - densidade', 'Justificativa para alteração da densidade',
'Poder Calorífico Inferior', 'Unidade de Medida - Poder Calorífico Inferior',
'Justificativa para alteração do Poder Calorífico Inferior',
'Justificativa para Alteração do Conteúdo de Carbono', 'Fator de Oxidação',
'Unidade de Medida - Fator de Oxidação',
'Justificativa para Alteração do Fator de Oxidação', 'Conteúdo de Carbono', 'Unidade de Medida - Conteúdo de Carbono'
]
#Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)


# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()

# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('5-contagem_empresas_por_setor.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()
# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('5-contagem_empresas_por_setor2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()
# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('5-contagem_empresas_por_setor2.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('5-result_emissoes_atm_setor.csv', index=False)
