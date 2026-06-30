import html
import os
from time import time
import time    
from tabelaBovideos import tabela_bovideos

def menu_relatorio(driver, WebDriverWait, EC, By, sleep,caminho_download):
    arquivo_atual = None 
    try:
        print("Acessando menu de relatórios...")
        driver.switch_to.default_content()
        print("Entrando no iframe: mainsystem")
        WebDriverWait(driver, 25).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainsystem"))
        )

        print("Entrando no iframe: mainform")
        WebDriverWait(driver, 25).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainform"))
        )

        script_clique = """
        var links = document.getElementsByTagName('a');
        for (var i = 0; i < links.length; i++) {
            if (links[i].textContent.includes('Saldo Atual de Animais')) {
                links[i].click();
                return "Sucesso: Elemento encontrado e clicado!";
            }
        }
        return "Erro: O elemento não foi encontrado no HTML deste iframe.";
        """
    
        driver.execute_script(script_clique)

        # 1. Volta para o topo absoluto para limpar os frames antigos
        driver.switch_to.default_content()
        
        # 2. Entra no mainsystem principal novamente
        WebDriverWait(driver, 25).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainsystem"))
        )
        
        # 3. Entra no novo iframe do pop-up (ID 793) que apareceu após o clique
        print("Entrando no iframe da janela flutuante (formID=793)")
        WebDriverWait(driver, 25).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, 'formID=793')]"))
        )
        
        # 4. Entra no mainform interno desta nova janela
        print("Entrando no novo iframe: mainform (interno do relatório)")
        WebDriverWait(driver, 25).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainform"))
        )

        # =======================================================================
        # =======================================================================
        print("Aguardando a lista 'lookupInput' carregar na nova tela...")
        bt_exploracao = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/div/div/div/div[3]/div/button"))
        )
        bt_exploracao.click()

        lista_exploracao = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/ul"))
        )

    
        opcoes_exploracao = lista_exploracao.find_elements(By.TAG_NAME, "li")
        
        print(f"Total de itens encontrados: {len(opcoes_exploracao)}")
        print("--- LISTA DE OPÇÕES ---")
        
        for opcao_exp in opcoes_exploracao:
            texto = opcao_exp.text.strip()
            
            if texto:
                texto_maiusculo = texto.upper()
                if ("ATIVO" in texto_maiusculo or "ATIVA" in texto_maiusculo) and "INATIV" not in texto_maiusculo:
                    print(f"Opção encontrada: {texto}")
                    opcao_exp.click()
                    break  
            else:
                print("Nenhuma opção encontrada na lista de exploração.")
                continue


        sleep(5)

        # =======================================================================
        # =======================================================================

        bt_gpexpecies = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/div/div/div/div[4]/div/button"))
        )
        bt_gpexpecies.click()

        lista_especies = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/ul"))
        )

        opcoes_lista = lista_especies.find_elements(By.TAG_NAME, "li")
        
        print(f"Total de itens encontrados: {len(opcoes_lista)}")
        print("--- LISTA DE OPÇÕES ---")
        
        for opcao in opcoes_lista:
            texto = opcao.text.strip()
            
            if texto:
                texto_maiusculo = texto.upper()
                if "BOVÍDEOS" in texto_maiusculo:
                    print(f"Opção encontrada: {texto}")
                    opcao.click()
                    break  # Sai do loop após selecionar a opção desejada
        sleep(5)
        quant_arq = len(os.listdir(caminho_download))

        bt_imprimir = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/div/div/div/div[6]/button"))
        )
        bt_imprimir.click()
        sleep(10)
        try:
            segundos = 0

            while len(os.listdir(caminho_download)) == quant_arq and segundos < 30:
                time.sleep(1)
                segundos += 1

            if len(os.listdir(caminho_download)) > quant_arq:
                print("O arquivo foi baixado")
                
                arquivo_atual = tabela_bovideos(caminho_download)
            else:
                print("Erro: O tempo limite estourou e o arquivo não apareceu.")
        except:
            print("Finalizado com ERRO")
    
    
    except Exception as e:
        print(fr"Erro: {e}")
    
    return arquivo_atual

