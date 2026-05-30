from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:

    BOTAO_CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')
    CAMPO_NOME      = (By.ID, 'first-name')
    CAMPO_SOBRENOME = (By.ID, 'last-name')
    CAMPO_CEP       = (By.ID, 'postal-code')
    BOTAO_CONTINUAR = (By.ID, 'continue')
    TITULO_OVERVIEW = (By.CLASS_NAME, 'title')
    BOTAO_FINALIZAR = (By.ID, 'finish')
    MSG_SUCESSO     = (By.CLASS_NAME, 'complete-header')

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def clicar_checkout(self):
        self.wait.until(EC.url_contains('/cart.html'))
        print(f"\nURL atual: {self.driver.current_url}")
        print(f"Título da página: {self.driver.title}")
        self.wait.until(EC.element_to_be_clickable(self.BOTAO_CHECKOUT)).click()

    def preencher_dados(self, nome, sobrenome, cep):
        self.driver.find_element(*self.CAMPO_NOME).send_keys(nome)
        self.driver.find_element(*self.CAMPO_SOBRENOME).send_keys(sobrenome)
        self.driver.find_element(*self.CAMPO_CEP).send_keys(cep)

    def clicar_continuar(self):
        self.driver.find_element(*self.BOTAO_CONTINUAR).click()

    def obter_titulo_overview(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TITULO_OVERVIEW)
        ).text

    def finalizar_compra(self):
        self.wait.until(EC.element_to_be_clickable(self.BOTAO_FINALIZAR)).click()

    def obter_mensagem_sucesso(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MSG_SUCESSO)
        ).text
   