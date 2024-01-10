""""
Lê as bases limpas.
Salvas localmente como bases (formato pickle), após rodar read_organize_databases.py

Analisar os indicadores (README.md)

"""

import os
import pickle
import numpy as np
import pandas as pd
import change_cnae_to_12_sectors
import matplotlib.pyplot as plt


print("Diretório atual:", os.getcwd())

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}


def emissions_by_municipality(data):
    pass


def quant_efluentes_cnae(data):
    print(data.groupby(by='isis_12').agg('mean')['quant_efluentes_liquidos'].sort_values(ascending=False).head(20))


if __name__ == '__main__':

    # LER BASE FINAL NA QUAL TODAS AS MUDANÇAS DE FORMA, CORREÇOES, INDICADORES NOVOS JÁ FORAM FEITAS.
    nome = 'bases_massa_desidentificada'
    with open(nome, 'rb') as handler:
        base = pickle.load(handler)

    pasta_saida = 'analise_descritiva'

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Defina a variável 'chaves' aqui
    chaves = ['quant_efluentes_liquidos', 'quant_poluentes_emitidos', 'quant_residuos_solidos',
              'quant_consumida_energia_acordo_tipo', 'quantidade_energia_padrao_calorias', 'co2_emissions',
              'perc_efficiency_treatment']

    total_municipios = 0
    for cada in paths:
        base[cada]['cnae2d'] = base[cada]['clas_cnae20'].str[:2]
        base[cada] = change_cnae_to_12_sectors.from_cnae_2digitos_to_12_mip_sectors(base[cada], 'cnae2d')
        if 'mun' in base[cada].columns:
            total_municipios += base[cada]['mun'].nunique()
            print(f"Total de municípios em {cada}: {base[cada]['mun'].nunique()}")
        else:
            print(f"A coluna 'mun' não está presente em {cada}.")


        # Filtrar os dados para os últimos 10 anos
        base[cada] = base[cada][base[cada]['ano'] >= base[cada]['ano'].max() - 9]

        # Adiciona o cálculo da ecoeficiência para cada categoria
        for cada in paths:
            base[cada]['cnae2d'] = base[cada]['clas_cnae20'].str[:2]
            base[cada] = change_cnae_to_12_sectors.from_cnae_2digitos_to_12_mip_sectors(base[cada], 'cnae2d')

        # Loop para cada variável de interesse
        for chave in chaves:
            # if chave == 'perc_efficiency_treatment':
            #     if chave in base[cada]:
            #
            #        # _________________________________________________________________________________________________
            #         caminho_arquivo = os.path.join(pasta_saida, f'nao_conformidade_{chave}_setor.csv')
            #         temp = base[cada][(base[cada][chave] <= 100) & (base[cada][chave] >= 0)].copy()
            #         temp.loc[:, 'nao_conformidade'] = 0
            #         temp.loc[:, 'conformidade'] = 0
            #         temp.loc[temp[chave] < 80, 'nao_conformidade'] = 1
            #         temp.loc[temp[chave] >= 80, 'conformidade'] = 1
            #         temp = temp[['nao_conformidade', 'conformidade', 'isis_12']].groupby('isis_12').agg('sum')
            #         temp.to_csv(caminho_arquivo)


            if chave in base[cada]:
            #     # Por UFs - Cálculo da razão
            #     # Por Setores - Cálculo da razão
            #     caminho_arquivo_razao = os.path.join(pasta_saida, f'razao_{chave}_setor.csv')
            #     base[cada]['cnpj'] = 'valores_cnpj_aqui'
            #     temp_setor_razao = base[cada][[chave, 'isis_12', 'cnpj']].groupby(['isis_12', 'cnpj']).agg({
            #         chave: 'sum'
            #     }).reset_index()
            #
            #     # Contagem única de CNPJ por setor
            #     temp_setor_razao_count = temp_setor_razao.groupby('isis_12')['cnpj'].nunique().reset_index(
            #         name='quantidade_empresas')
            #
            #     # Merge dos dados para calcular a razão
            #     temp_setor_razao_final = pd.merge(temp_setor_razao.groupby('isis_12').agg({chave: 'sum'}).reset_index(),
            #                                       temp_setor_razao_count, on='isis_12')
            #
            #     # Cálculo da razão
            #     temp_setor_razao_final['razao'] = temp_setor_razao_final[chave] / temp_setor_razao_final[
            #         'quantidade_empresas']
            #     temp_setor_razao_final.to_csv(caminho_arquivo_razao)


                # Por setores
                caminho_arquivo = os.path.join(pasta_saida, f'descritivas_{chave}_setor.csv')
                temp_setor = base[cada][[chave, 'isis_12']].groupby('isis_12').agg(['max', 'mean',
                                                                              np.median, 'std', 'min'])[chave]

                # Por setores - cálculo da ecoeficiência
                caminho_arquivo_ecoeficiencia = os.path.join(pasta_saida, f'ecoeficiencia_{chave}_setor.csv')
                temp_categoria = base[cada][[chave, 'massa_salarial', 'isis_12']].groupby('isis_12').agg(
                    {'massa_salarial': 'sum', chave: 'sum'})
                temp_categoria['ecoeficiencia'] = temp_categoria['massa_salarial'] / temp_categoria[chave]
                temp_categoria.to_csv(caminho_arquivo_ecoeficiencia)


                # Por UFs
                #caminho_arquivo = os.path.join(pasta_saida, f'descritivas_{chave}_UF.csv')
                #temp = base[cada][[chave, 'estado']].groupby('estado').agg(['max', 'mean',
                                                                            #np.median, 'std', 'min'])[chave]

                temp_setor.to_csv(caminho_arquivo)

                # Cálculo da ecoeficiência por ano nos últimos 10 anos e salvar em um único arquivo CSV
                caminho_arquivo_ecoeficiencia_10_anos = os.path.join(pasta_saida,
                                                                     f'ecoeficiencia_{chave}_ultimos_10_anos.csv')

                resultados = pd.DataFrame()  # Dataframe para armazenar os resultados

                # Cálculo da ecoeficiência por ano nos últimos 10 anos
                for ano in range(base[cada]['ano'].max() - 9, base[cada]['ano'].max() + 1):

                    temp_ano = base[cada].copy()
                    temp_ano = temp_ano[temp_ano['ano'] == ano]
                    temp_ano = temp_ano[[chave, 'massa_salarial', 'isis_12']].groupby('isis_12').agg(
                        {'massa_salarial': 'sum', chave: 'sum'}
                    )
                    temp_ano['ecoeficiencia'] = temp_ano['massa_salarial'] / temp_ano[chave]
                    temp_ano['ano'] = ano  # adicinona coluna ano

                    # Adicionar os resultados ao DataFrame principal
                    # resultados = resultados.append(temp_ano)

               # Salvar os resultados em um arquivo CSV
                resultados.to_csv(caminho_arquivo_ecoeficiencia_10_anos, index=True)

        # ==========================================================================
        # Importar os dados
    dados = pd.read_csv('analise_descritiva/ecoeficiencia_co2_emissions_setor.csv')

    #
    # # Criar o gráfico
    # plt.bar(dados['isis_12'], dados['co2_emissions'])
    # plt.xlabel('Setor econômico')
    # plt.ylabel('Emissões de CO2 (toneladas)')
    # plt.show()

    print(f"Total de municípios em todas as bases: {total_municipios}")


# Mapear fatores de conversão para toneladas em notação científica
fatores_conversao = {'kilogramas': 1e-3, 'Tonelada': 1, 'Grama': 1e-6, 'Miligrama': 1e-9}

# Converter a coluna "Quantidade" para valores numéricos
data['Quantidade'] = pd.to_numeric(data['Quantidade'], errors='coerce')

# Criar uma nova coluna "Quantidade em Toneladas" com os valores convertidos
data['Quantidade em Toneladas'] = data.apply(lambda row: row['Quantidade'] * fatores_conversao[row['Unidade']], axis=1)

# Salvar o DataFrame modificado de volta para um arquivo CSV
data.to_csv('3-nova_base_convertida.csv', index=False)