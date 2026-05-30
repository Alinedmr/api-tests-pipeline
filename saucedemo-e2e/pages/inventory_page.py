from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:

    TITULO           = (By.CLASS_NAME, 'title')
    ICONE_CARRINHO   = (By.CLASS_NAME, 'shopping_cart_link')
    BADGE_CARRINHO   = (By.CLASS_NAME, 'shopping_cart_badge')

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def obter_titulo(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TITULO)
        ).text

    def adicionar_produto(self, nome_produto):
        seletor = (By.XPATH, f'//div[text()="{nome_produto}"]/ancestor::div[@class="inventory_item"]//button')
        botao = self.wait.until(EC.element_to_be_clickable(seletor))
        botao.click()
        # Aguarda o badge atualizar antes de continuar
        import time
        time.sleep(0.5)

    def obter_quantidade_carrinho(self):
        badge = self.wait.until(
            EC.visibility_of_element_located(self.BADGE_CARRINHO)
        )
        return int(badge.text)

    def ir_para_carrinho(self):
        self.driver.find_element(*self.ICONE_CARRINHO).click()