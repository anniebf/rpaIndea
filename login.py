import logging

from trio import sleep


def login_indea(login_usuario,senha_usuario, driver, row, WebDriverWait, EC, By, sleep,logging):

    #
    # LOGIN NO INDEA
    #
    try:
        #Entrando no frame principal
        logging.info(fr"Realizando login do usuário: {row['Login']}...")
        driver.switch_to.default_content()
        WebDriverWait(driver, 25).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainform"))
        )

        input_login = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.ID, "WFRInput25841"))
        )
        input_login.click()
        input_login.send_keys(login_usuario)

        input_senha = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/form/div/div/div/div/div[4]/input')))
        input_senha.click()
        input_senha.send_keys(senha_usuario)

        logging.info(fr"Inserindo login e senha do usuário")
        bt_entrar = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/form/div/div/div/div/div[5]/button')))
        bt_entrar.click()
        logging.info(fr"Botão de login clicado, aguardando resposta do sistema...")

        sleep(5)

        try:
            
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(),'Acesso')]")
                )
            )
            logging.info(fr"Verificando se o login é válido para o usuário: {row['Login']}...")
            #print("Login inválido")

            login_realizado = False

        except:
            logging.info(fr"Login realizado com sucesso para o usuário: {row['Login']}")
            login_realizado = True
            #print("Login realizado")


    except Exception as e:
        print(fr"Erro: {e}")
        login_realizado = False

    return login_realizado
