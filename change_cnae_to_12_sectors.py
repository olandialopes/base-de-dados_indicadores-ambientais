import pandas as pd


def from_cnae_2digitos_to_12_mip_sectors(data: object, col: object) -> object:
    # Source: IBGE/CONCLA ESTRUTURA and ISIS rev. 4 following
    # de VRIES, Gaaitzen et al. The economic transformation database (ETD): content, sources, and methods.
    # Wider technical note 2/2021.
    tradutor_concla_ibge = {'A': ['01', '02', '03'],
                            'B': ['05', '06', '07', '08', '09'],
                            'C': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                                  '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
                            'D': ['35'],
                            'E': ['36', '37', '38', '39'],
                            'F': ['41', '42', '43'],
                            'G': ['45', '46', '47'],
                            'H': ['49', '50', '51', '52', '53'],
                            'I': ['55', '56'],
                            'J': ['58', '59', '60', '61', '62', '63'],
                            'K': ['64', '65', '66'],
                            'L': ['68'],
                            'M': ['69', '70', '71', '72', '73', '74', '75'],
                            'N': ['77', '78', '79', '80', '81', '82'],
                            'O': ['84'],
                            'P': ['85'],
                            'Q': ['86', '87', '88'],
                            'R': ['90', '91', '92', '93'],
                            'S': ['94', '95', '96'],
                            'T': ['97'],
                            'U': ['99']
                            }

    tradutor_isis_12 = {'Agriculture': ['A'],
                        'Mining': ['B'],
                        'Manufacturing': ['C'],
                        'Utilities': ['D', 'E'],
                        'Construction': ['F'],
                        'Trade': ['G', 'I'],
                        'Transport': ['H'],
                        'Business': ['J', 'M', 'N'],
                        'Financial': ['K'],
                        'RealEstate': ['L'],
                        'Government': ['O', 'P', 'Q'],
                        'OtherServices': ['R', 'S', 'T', 'U']
                        }

    data['letter_code'] = data[col].apply(lambda x: next((key for key, value in tradutor_concla_ibge.items()
                                                          if x in value), None))
    data['isis_12'] = data['letter_code'].apply(lambda x: next((key for key, value in tradutor_isis_12.items()
                                                                if x in value), None))
    return data
if __name__ == '__main__':
    # Arquivo CSV para incluir os 12 setores
     # f = 'mean.csv'
    # Arquivo CSV para incluir os 12 setores
    f = 'median_setoresISIS.csv'

    # Ler arquivo
    mea = pd.read_csv(f, dtype={'isis_12': str, 'codemun': str})
    # Nome da coluna que contenha os dois dígitos da CNAE em STR.
           #    (se não tiver essa coluna, basta fazer: data['cnae_2d'] = data['cnae'].apply(lambda x: x.str[2:]
    coluna_a_traduzir = 'isis_12'
    mea = from_cnae_2digitos_to_12_mip_sectors(mea, coluna_a_traduzir)


