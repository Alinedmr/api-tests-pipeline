from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:

    URL = 'https://www.saucedemo.com/'

    CAMPO_USUARIO = (By.ID, 'user-name')
    CAMPO_SENHA   = (By.ID, 'password')
    BOTAO_LOGIN   = (By.ID, 'login-button')
    MSG_ERRO      = (By.CSS_SELECTOR, '[data-test=error]')

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.URL)

    def fazer_login(self, usuario, senha):
        campo_u = self.wait.until(EC.visibility_of_element_located(self.CAMPO_USUARIO))
        campo_u.clear()
        campo_u.send_keys(usuario)

        campo_s = self.driver.find_element(*self.CAMPO_SENHA)
        campo_s.clear()
        campo_s.send_keys(senha)

        self.driver.find_element(*self.BOTAO_LOGIN).click()

    def obter_mensagem_erro(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MSG_ERRO)
        ).text