import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-features=PasswordManager,AutofillServerCommunication')
    options.add_argument('--disable-save-password-bubble')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-features=PasswordManager,AutofillServerCommunication,SafeBrowsingPasswordProtection')
    options.add_argument('--password-store=basic')
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_manager_leak_detection': False,
        'safebrowsing.enabled': False,
        'profile.default_content_setting_values.notifications': 2,
        'autofill.profile_enabled': False,
    })
    options.add_experimental_option('excludeSwitches', ['enable-automation'])


    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)  

    yield driver  

    driver.quit()  