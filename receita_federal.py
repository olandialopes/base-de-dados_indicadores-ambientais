from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
from requests import get

credentials = {
                'HOST': '127.0.1.1',
                'PORT': '5432',
                'USER': 'dani',
                'PASSWORD': '',
                'DATABASE': 'Dados_RFB'
              }

tables = [
    'cnae',
    'empresa',
    'estabelecimento',
    'moti',
    'munic',
    'natju',
    'pais'
]


def get_ibama_data(html):
    with open(html) as file:
        html = file.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all(lambda tag: tag.name == 'div' and tag.find_all('section', tabindex="1000"))
    data = soup.find_all('a')
    data = list(map(lambda a: a.get('href'), data))
    return data

def get_description(html):
    soup = BeautifulSoup(html, 'html.parser')
    trs_subclasse = soup.find_all(lambda tag: tag.name == 'tr' and tag.find('td', colspan="6") and tag.find('p', class_='Tabela_Texto_Justificado', text='Subclasse'))
    trs_atividades = soup.find_all(lambda tag: tag.name == 'tr' and tag.find('td', colspan="6") and tag.find('p', class_='Tabela_Texto_Justificado', text='Atividade'))
    tr_ppgu = soup.find_all(lambda tag: tag.name == 'tr' and tag.find('td', colspan='5') and tag.find('p', class_='Tabela_Texto_Justificado'))
    if len(tr_ppgu) >= 2:
        ppgu = tr_ppgu[2].find_all('td')
        ppgu = ppgu[1].text.strip() if len(ppgu) >= 2 else 'None'
    else:
        ppgu = 'None'
    trs = trs_subclasse + trs_atividades
    result = []
    if len(trs):
        for tr in trs:
            ps = tr.find_all('p', class_='Tabela_Texto_Justificado')
            result.append(ps[-1].text + '/' + ppgu)
    print(f'Done <{html}>')
    return result

def main():
    engine = create_engine('postgresql://'+credentials['USER']+':'+credentials['PASSWORD']+'@'+credentials['HOST']+':'+credentials['PORT']+'/'+credentials['DATABASE'])
    conn = psycopg2.connect('dbname='+credentials['DATABASE']+' '+'user='+credentials['USER']+' '+'host='+credentials['HOST']+' '+'port='+credentials['PORT']+' '+'password='+credentials['PASSWORD'])
    cur = conn.cursor()

    # dataset = {'Descrição': [], 'N° de empresas': []}
    # acc = 0
    # with open('descriptions.txt') as file:
    #     for description in file.readlines():
    #         description = description.strip()
    #         cmd = f"select count(*) from empresa, cnae, estabelecimento where (empresa.cnpj_basico = estabelecimento.cnpj_basico) and (cnae.codigo::integer = estabelecimento.cnae_fiscal_principal) and (cnae.descricao = %s);"
    #         cur.execute(cmd, (description,))
    #         num = cur.fetchone()[0]
    #         acc += num
    #         dataset['Descrição'].append(description)
    #         dataset['N° de empresas'].append(num)
    #         print(f'{description} -> done! [Total: {acc}]')
    # df = pd.DataFrame.from_dict(dataset)
    # df.to_csv('numero_empresas.csv')

    # s = pd.read_csv('numero_empresas.csv')
    # ss = s.drop_duplicates(subset=['Descrição']).loc[:, ~s.columns.str.contains('^Unnamed')].reset_index(drop=True)
    # ss = ss[ss['N° de empresas'] > 0].reset_index(drop=True)
    # print(ss['N° de empresas'].sum())
    #ss.to_csv('numero_empresas_not_null.csv')

    # links = get_ibama_data('ibama.html')
    # df = {'CNAE': [], 'PP/GU': []}
    # with open('descriptions.txt', 'w+') as file:
    #     for link in links:
    #         temp = get_description(get(link).text)
    #         for item in temp:
    #             file.write(item + '\n')

    # new_df = {'CNAE': [], 'PP/GU': []}

    # enter = pd.read_csv('numero_empresas_not_null.csv')
    # enter = list(enter['Descrição'])

    # data = pd.read_csv('empresas_ppgu.csv').drop_duplicates(subset=['CNAE'])
    # data = data.loc[:, ~data.columns.str.contains('^Unnamed')].reset_index(drop=True)
    # data.to_csv('ppgu.csv')
    # with open('descriptions.txt') as file:
    #     for line in file.readlines():
    #         temp = line.split('/') 
    #         if len(temp) == 2:
    #             description, ppgu = temp
    #             ppgu = ppgu.strip()
    #             if description in enter:
    #                 new_df['CNAE'].append(description)
    #                 new_df['PP/GU'].append(ppgu)
    #     df = pd.DataFrame.from_dict(new_df)
    #     df.to_csv('empresas_ppgu.csv')

    # 

    data = pd.read_csv('final_ppgu.csv')

    for cnae in data['CNAE']:
        cmd = f"select empresa  . from empresa, cnae, estabelecimento where (empresa.cnpj_basico = estabelecimento.cnpj_basico) and (cnae.codigo::integer = estabelecimento.cnae_fiscal_principal) and (cnae.descricao = %s);"
        cur.execute(cmd, (cnae,))
        num = cur.fetchone()[0]
              

if __name__ == '__main__':
    main()
