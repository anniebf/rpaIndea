from time import sleep
import glob
import pdfplumber
import os
import pandas as  pd

from database import inserirDadosBovideos

def tabela_bovideos(pasta_download):
    arquivo_atual = encontrar_arquivo(pasta_download)
    #print(f"Arquivo encontrado: {arquivo_atual}")

    return arquivo_atual

def encontrar_arquivo(pasta_download):

    nome_arquivo = None

    print('Buscando o último arquivo baixado...')
    sleep(2) 

    arquivos = glob.glob(os.path.join(pasta_download, '*.pdf'))
    
    if not arquivos:
        print("Nenhum arquivo PDF encontrado na pasta.")
        return None
        
    ultimo_arquivo_completo = max(arquivos, key=os.path.getctime)
    
    nome_arquivo = os.path.basename(ultimo_arquivo_completo)
    
    print(f'Arquivo encontrado: {nome_arquivo}')

    return nome_arquivo

def processar_arquivo(cnpj,caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        tabelas = []
        
        for pagina in pdf.pages:
            tabela_pagina = pagina.extract_table()
            if tabela_pagina:
                # Transformando a listas em DataFrame
                df_pagina = pd.DataFrame(tabela_pagina[1:])
                tabelas.append(df_pagina)
        
        print(f"Total de tabelas extraídas: {len(tabelas)}")
        
        if tabelas:
            df = tabelas[0]

            #CONDICOES DA TABELA
            cond_vazias = df[df.columns[0]].notna() & (df[df.columns[0]] != '') & df[df.columns[1]].notna() & (df[df.columns[1]] != '')
            cond_bovino = df[df.columns[0]].str.strip() == 'BOVINO'

            #APLICANDO FILTROS 
            df_filtro = df[cond_vazias & cond_bovino]
            #print(df_filtro)


            inserir_dados_banco(cnpj, df_filtro)
            return 
   
def inserir_dados_banco(cnpj, tabela):

    for index, row in tabela.iterrows():
        
        faixetaria = row[1]
        sexo = '1' if row[2] == "MACHO" else '2'
        quant = row[3]
        
        faixet = None 

        if sexo == '1':
            if faixetaria == "00 A 04 MESES":
                faixet = "144094"
            elif faixetaria == "05 A 12 MESES":
                faixet = "144096"
            elif faixetaria == "13 A 24 MESES":
                faixet = "000047"
            elif faixetaria == "25 A 36 MESES":
                faixet = "000046"
            elif faixetaria == "ACIMA DE 36 MESES":
                faixet = "000041"
                
        elif sexo == '2':
            if faixetaria == "00 A 04 MESES":
                faixet = "144095"
            elif faixetaria == "05 A 12 MESES":
                faixet = "144097"
            elif faixetaria == "13 A 24 MESES":
                faixet = "000049"
            elif faixetaria == "25 A 36 MESES":
                faixet = "000069"
            elif faixetaria == "ACIMA DE 36 MESES":
                faixet = "000043"

        if faixet: 
            print("-" * 30)
            print(f"Dados extraídos - CNPJ: {cnpj}, Sexo: {sexo}, Faixa Etária: {faixet}, Quantidade: {quant}")
            inserirDadosBovideos(cnpj, sexo, faixet, quant)
            print("-" * 30)
            
    return