import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage

USUARIO = 'standard_user'
SENHA   = 'secret_sauce'


class TestLoginFlow:

    def test_login_valido(self, driver):
        login = LoginPage(driver)
        login.abrir()
        login.fazer_login(USUARIO, SENHA)

        inventory = InventoryPage(driver)
        assert inventory.obter_titulo() == 'Products'

    def test_login_invalido(self, driver):
        login = LoginPage(driver)
        login.abrir()
        login.fazer_login('standard_user', 'senha_errada')

        erro = login.obter_mensagem_erro()
        assert 'Username and password do not match' in erro

    def test_usuario_bloqueado(self, driver):
        login = LoginPage(driver)
        login.abrir()
        login.fazer_login('locked_out_user', SENHA)

        erro = login.obter_mensagem_erro()
        assert 'locked out' in erro


class TestCompraCompleta:

    def test_fluxo_completo_compra(self, driver):
        login = LoginPage(driver)
        login.abrir()
        login.fazer_login(USUARIO, SENHA)

        inventory = InventoryPage(driver)
        assert inventory.obter_titulo() == 'Products'

        inventory.adicionar_produto('Sauce Labs Backpack')
        inventory.adicionar_produto('Sauce Labs Bike Light')
        assert inventory.obter_quantidade_carrinho() == 2

        inventory.ir_para_carrinho()
        checkout = CheckoutPage(driver)
        checkout.clicar_checkout()
        checkout.preencher_dados('Aline', 'Rodrigues', '64000000')
        checkout.clicar_continuar()

        assert checkout.obter_titulo_overview() == 'Checkout: Overview'
        checkout.finalizar_compra()

        mensagem = checkout.obter_mensagem_sucesso()
        assert 'Thank you for your order' in mensagem