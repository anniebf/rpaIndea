import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from trio import sleep
from menuLateral import menu_relatorio
from login import login_indea
from tabelaBovideos import processar_arquivo

caminho_planilha = 'C:\\rpaIndea\\senhas\\Senhas-INDEA.xlsx'
tabela_indea = pd.read_excel(caminho_planilha)
df = pd.DataFrame(tabela_indea)
caminho_download = "C:\\rpaIndea\\download"

def configurar_options():
    """Gera um objeto de options limpo a cada iteração para evitar bugs"""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--mute-audio')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Configurações de download fixadas aqui
    options.add_experimental_option("prefs", {
        "download.default_directory": caminho_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,  
        "download.extensions_to_open": "applications/pdf", 
        "profile.default_content_setting_values.automatic_downloads": 1 
    })
    return options

def main():
    print("----------------INICIANDO----------------")    
    for index, row in df.iterrows():
        driver = None
        
        aglomerado = row['Aglomerado']
        login_usuario = row['Login']
        senha_usuario = row['Senha']
        municipio = row['Municipio']

        try:
            options = configurar_options() # Instancia as opções limpas

            print(fr"Iniciando o Selenium para o usuário: {row['Login']}...")
            driver = webdriver.Chrome(options=options)
            url = "https://sistemas.indea.mt.gov.br/PRD/open.do?action=open&sys=PRD"
            driver.implicitly_wait(2)
            
            driver.get(url)
            driver.maximize_window()

            login_realizado = login_indea(login_usuario, senha_usuario, driver, row, WebDriverWait, EC, By, sleep)
            sleep(2) 
            
            if login_realizado:
                # Se o erro persistir, o crash está acontecendo exatamente dentro desta função:
                arquivo_atual = menu_relatorio(driver, WebDriverWait, EC, By, sleep, caminho_download)
                if arquivo_atual:
                    print(fr"Iniciando o processamento do arquivo: {arquivo_atual}")
                    caminho_arquivo = os.path.join(caminho_download, arquivo_atual)
                    processar_arquivo(login_usuario,caminho_arquivo)

            print(fr"Login do usuário {row['Login']} processado com sucesso.")
    
        except Exception as e:
            print(fr"Erro durante a execução do usuário {row['Login']}: {e}")
            
        finally:
            if driver:
                try:
                    driver.quit()
                    print("Navegador encerrado corretamente.")
                except Exception:
                    pass 
    print("Todos os Cpnjs foram processados")
    print("----------------FINALIZANDO----------------")

if __name__ == "__main__": 
    main()