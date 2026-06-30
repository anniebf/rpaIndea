from trio import sleep


def login_indea(login_usuario,senha_usuario, driver, row, WebDriverWait, EC, By, sleep):

    #
    # LOGIN NO INDEA
    #
    try:
        #Entrando no frame principal
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

        bt_entrar = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/form/div/div/div/div/div[5]/button')))
        bt_entrar.click()

        sleep(5)

        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(),'Acesso')]")
                )
            )

            print("Login inválido")

            login_realizado = False

        except:
            login_realizado = True
            print("Login realizado")


    except Exception as e:
        print(fr"Erro: {e}")
        login_realizado = False

    return login_realizado
