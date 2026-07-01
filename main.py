from datetime import datetime
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
import logging
from time import sleep
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(fr"log/{datetime.now().strftime('%d-%m-%Y')}_relatorio_animais_indea.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logging.captureWarnings(True)
#avisos capturados só aparecem se forem erros graves
logging.getLogger("py.warnings").setLevel(logging.ERROR)

caminho_planilha = 'C:\\rpaIndea\\senhas\\Senhas-INDEA.xlsx'
tabela_indea = pd.read_excel(caminho_planilha)
df = pd.DataFrame(tabela_indea)
caminho_download = "C:\\rpaIndea\\download"

def configurar_options():
    """Gera um objeto de options limpo a cada iteração para evitar bugs"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--mute-audio')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
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
    logging.info("----------------INICIANDO----------------")
    #print("----------------INICIANDO----------------")    
    for index, row in df.iterrows():
        driver = None
        
        aglomerado = row['Aglomerado']
        login_usuario = row['Login']
        senha_usuario = row['Senha']
        municipio = row['Municipio']

        try:
            options = configurar_options() 

            logging.info(fr"Iniciando o Selenium para o usuário: {row['Login']}...")
            driver = webdriver.Chrome(options=options)
            url = "https://sistemas.indea.mt.gov.br/PRD/open.do?action=open&sys=PRD"
            driver.implicitly_wait(2)
            
            driver.get(url)
            driver.maximize_window()

            login_realizado = login_indea(login_usuario, senha_usuario, driver, row, WebDriverWait, EC, By, sleep,logging)
            sleep(2) 
            
            if login_realizado:
            
                arquivo_atual = menu_relatorio(driver, WebDriverWait, EC, By, sleep, caminho_download,logging)
                if arquivo_atual:
                    logging.info(fr"Iniciando o processamento do arquivo: {arquivo_atual}")
                    caminho_arquivo = os.path.join(caminho_download, arquivo_atual)
                    processar_arquivo(login_usuario,caminho_arquivo,logging)
                    logging.info(fr"Processamento do arquivo {arquivo_atual} concluído com sucesso.")
                    os.remove(fr"{caminho_arquivo}")
                    logging.info(fr"Arquivo {arquivo_atual} removido com sucesso.")

            logging.info(fr"Login do usuário {row['Login']} processado com sucesso.")
    
        except Exception as e:
            logging.error(fr"Erro durante a execução do usuário {row['Login']}: {e}")
            
        finally:
            if driver:
                try:
                    driver.quit()
                    logging.info("Navegador encerrado corretamente.")
                except Exception:
                    pass 
    logging.info("Todos os Cpnjs foram processados")
    logging.info("----------------FINALIZANDO----------------")

if __name__ == "__main__": 
    main()