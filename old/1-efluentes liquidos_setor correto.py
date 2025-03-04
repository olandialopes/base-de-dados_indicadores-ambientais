import pandas as pd

data = pd.read_csv('1-relatorio efluentes liquidos_ibama.csv', delimiter=';')

# Colunas a serem excluidas
colunas_indesejadas = [
    'Código da Categoria', 'Código do Detalhe', 'Desc. Monitoramento Utilizado',
    'Compart. Ambiental da Emissão', 'Tipo de Emissão', 'Tipo Corpo Receptor',
    'Classe do Corpo Receptor', 'Nome do Corpo Hídrico', 'Corpo Receptor',
    'Qual?', 'Empresa Receptora do Efluente', 'Tipo de Emissão Para o Solo',
    '(Se outro) Qual?', 'Situação Cadastral', 'Latitude', 'Longitude',
    'Nível de Tratamento', 'Tipo de Tratamento', 'Detalhe'
]
# Excluir as colunas indesejadas, cujos nomes estão acima
data = data.drop(columns=colunas_indesejadas, axis=1)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]


# Mapeamento das categorias para códigos de setor econômico
def categorize_setor_economico(categoria):
    if 'Administradora de Projetos Florestais' in categoria:
        return 1
    elif 'Extração e Tratamento de Minerais' in categoria:
        return 2
    elif any(keyword in categoria for keyword in
             ['Indústria Química', 'Indústria Metalúrgica', 'Indústria de Produtos Minerais Não Metálicos',
              'Indústria Mecânica', 'Indústria Têxtil', 'Indústria de Vestuário', 'Calçados e Artefatos de Tecidos',
              'Indústria de Madeira', 'Indústria de Produtos de Matéria Plástica', 'Indústria de material Elétrico',
              'Eletrônico e Comunicações', 'Indústrias Diversas', 'Indústria de Material de Transporte',
              'Indústria de Papel e Celulose', 'Indústria de Borracha', 'Indústria de Couros e Peles',
              'Indústria do Fumo', 'Indústria de Produtos Alimentares e Bebidas']):
        return 3
    elif 'Serviços de Utilidade' in categoria:
        return 4
    elif 'Obras civis - não relacionadas no Anexo VIII da Lei nº 6.938/1981,807' in categoria:
        return 5
    elif 'Veículos Automotores - Pneus - Pilhas e Baterias' in categoria:
        return 6
    elif 'Transporte, Terminais, Depósitos e Comércio' in categoria:
        return 7
    elif any(keyword in categoria for keyword in ['Serviços Administrativos', 'Turismo']):
        return 8
    else:
        return None  # Retorna None para categorias não mapeadas


# Adicionar a coluna 'Código do setor econômico' com base na coluna 'Categoria de atividade'
data['Código do setor econômico'] = data['Categoria de Atividade'].apply(categorize_setor_economico)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('1-Result_efluentes_liq_Tratamento_setores.csv', index=False)
