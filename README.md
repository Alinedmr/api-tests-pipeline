# api-tests-pipeline

Repositório de testes automatizados com duas frentes: testes de API REST com **Newman (Postman)** e testes E2E de interface web com **Selenium + Python**. Ambos integrados a uma pipeline de CI/CD via **GitHub Actions**.

---

## Estrutura do repositório

```
api-tests-pipeline/
├── .github/
│   └── workflows/
│       ├── newman.yml              # Pipeline de testes de API
│       └── selenium.yml            # Pipeline de testes E2E
├── postman/
│   ├── collection.json             # Collection exportada do Postman
│   └── environment.json            # Environment exportado do Postman
├── saucedemo-e2e/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   └── checkout_page.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_e2e_flow.py
│   ├── reports/                    # Relatórios gerados (não commitados)
│   ├── conftest.py
│   ├── pytest.ini
│   └── requirements.txt
├── package.json
├── .gitignore
└── README.md
```

---

## Projeto 1 — Testes de API com Newman

### Sobre

Testes automatizados da API REST [Petstore (Swagger)](https://petstore.swagger.io/v2) utilizando a collection exportada do Postman e executada via **Newman** na pipeline de CI/CD.

### Tecnologias

- [Postman](https://www.postman.com/) — criação e organização dos testes de API
- [Newman](https://github.com/postmanlabs/newman) — executor de collections Postman via linha de comando
- [newman-reporter-htmlextra](https://github.com/DannyDainton/newman-reporter-htmlextra) — gerador de relatório HTML

### Endpoints testados

| Módulo | Endpoints |
|---|---|
| Pets | Criar, buscar por ID, buscar por status |
| Store | Consultar inventário, realizar pedido |
| Users | Criar usuário, login, buscar, atualizar, deletar |

### Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `url_base` | URL base da API (`https://petstore.swagger.io/v2`) |
| `pet_id` | ID do pet criado — preenchido dinamicamente nos testes |
| `special-key` | Chave de autenticação — configurar via GitHub Secrets |

### Executar localmente

```bash
# Instalar dependências
npm install

# Rodar os testes
npm test
```

O relatório HTML será gerado em `reports/newman-report.html`.

---

## Projeto 2 — Testes E2E com Selenium

### Sobre

Testes de ponta a ponta (E2E) da aplicação web [SauceDemo](https://www.saucedemo.com/) utilizando **Selenium WebDriver** com **Python** e o padrão **Page Object Model (POM)**.

### Tecnologias

- [Python 3.11+](https://www.python.org/)
- [Selenium 4](https://www.selenium.dev/) — automação do navegador
- [pytest](https://pytest.org/) — framework de testes
- [pytest-html](https://pytest-html.readthedocs.io/) — geração de relatório HTML
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) — gerenciamento automático do ChromeDriver

### Fluxos testados

| Classe | Teste | Descrição |
|---|---|---|
| `TestLoginFlow` | `test_login_valido` | Login com credenciais corretas redireciona para a lista de produtos |
| `TestLoginFlow` | `test_login_invalido` | Login com senha errada exibe mensagem de erro |
| `TestLoginFlow` | `test_usuario_bloqueado` | Usuário bloqueado vê mensagem específica de bloqueio |
| `TestCompraCompleta` | `test_fluxo_completo_compra` | Login → adicionar produtos → carrinho → checkout → confirmação |

### Usuários de teste disponíveis

| Usuário | Senha | Comportamento |
|---|---|---|
| `standard_user` | `secret_sauce` | Fluxo normal — todos os testes passam |
| `locked_out_user` | `secret_sauce` | Usuário bloqueado — exibe mensagem de erro |
| `problem_user` | `secret_sauce` | Bugs propositais — imagens e comportamentos quebrados |
| `performance_glitch_user` | `secret_sauce` | Login com delay proposital |

### Executar localmente

```bash
# Entrar na pasta do projeto Selenium
cd saucedemo-e2e

# Criar o ambiente virtual
python -m venv venv --without-pip

# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1        # Windows (PowerShell)
source venv/bin/activate           # Mac/Linux

# Instalar o pip e as dependências
.\venv\Scripts\python.exe -m ensurepip --upgrade
pip install -r requirements.txt

# Rodar os testes
python -m pytest
```

O relatório HTML será gerado em `saucedemo-e2e/reports/relatorio.html`.

> **Atenção:** sempre rode os testes pelo terminal com o venv ativado usando `python -m pytest`. Não use o botão ▶️ do VS Code — ele usa o Python global e não encontra os módulos do projeto.

### Configurar o interpretador Python no VS Code

Para o VS Code reconhecer o venv automaticamente:

1. `Ctrl + Shift + P` → digita `Python: Select Interpreter`
2. Seleciona o caminho `.\venv\Scripts\python.exe`
3. Fecha e reabre o terminal integrado

---

## Autenticação no GitHub — Personal Access Token

O GitHub não aceita mais senha para operações Git via HTTPS. Para fazer push, é necessário um **Personal Access Token (PAT)**:

1. Acesse `github.com` → sua foto → **Settings**
2. **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)**
4. Marque apenas o escopo **`repo`** (controle total dos repositórios)
5. Defina expiração de 90 dias e clique em **Generate token**
6. Copie o token e configure no terminal:

```bash
git remote set-url origin https://SEU_TOKEN@github.com/SEU_USUARIO/api-tests-pipeline.git
git config --global credential.helper store
```

---

## CI/CD — GitHub Actions

O repositório conta com duas pipelines independentes que disparam automaticamente a cada `push` ou `pull request` nas branches `main` e `master`.

### Pipeline 1 — Newman (`newman.yml`)

```
Push/PR → Checkout → Node.js 20 → npm ci → Newman → Relatório HTML
```

### Pipeline 2 — Selenium (`selenium.yml`)

```
Push/PR → Checkout → Python 3.11 → pip install → python -m pytest → Relatório HTML
```

> **Importante:** a pipeline usa `python -m pytest` em vez de `pytest` diretamente, pois garante que o pytest instalado no ambiente virtual seja utilizado, evitando o erro `pytest: command not found`.

### Acessar os relatórios

Após cada execução, os relatórios ficam disponíveis em:

`GitHub → Actions → [execução] → Artifacts`

| Artifact | Conteúdo |
|---|---|
| `newman-report` | Resultado dos testes de API |
| `relatorio-selenium` | Resultado dos testes E2E |

Os artefatos ficam disponíveis por **30 dias**.

---

## Problemas conhecidos e soluções

### Popup de senha vazada bloqueando os testes

O Chrome exibe um alerta de "senha vazada" durante o login no SauceDemo, bloqueando a interação com a página. Solução aplicada no `conftest.py`:

```python
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
```

### Chrome não inicia na pipeline CI

As flags abaixo são **obrigatórias** em ambientes Linux sem interface gráfica (como o GitHub Actions). Nunca as remova do `conftest.py`:

```python
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

### ModuleNotFoundError: No module named 'pages'

Ocorre ao rodar o arquivo de teste diretamente com `python arquivo.py`. O pytest resolve os caminhos de módulos automaticamente. Sempre use:

```bash
python -m pytest
```

### Badge do carrinho não atualiza entre dois cliques

Ao adicionar dois produtos em sequência, o DOM pode não atualizar o badge antes do segundo clique. Solução aplicada no `inventory_page.py`:

```python
import time
time.sleep(0.5)  # aguarda o DOM atualizar entre os cliques
```

### pytest: command not found na pipeline

Ocorre porque o `pip install` salva o binário em um PATH diferente do shell da pipeline. Solução: sempre usar `python -m pytest` no lugar de `pytest` no arquivo `.yml`.

---

## Pré-requisitos locais

- Node.js 20+
- Python 3.11+
- Google Chrome instalado
- Git

---

## Dependências Python (`requirements.txt`)

```
attrs==26.1.0
certifi==2026.5.20
cffi==2.0.0
charset-normalizer==3.4.7
colorama==0.4.6
h11==0.16.0
idna==3.17
iniconfig==2.3.0
Jinja2==3.1.6
MarkupSafe==3.0.3
outcome==1.3.0.post0
packaging==26.2
pluggy==1.6.0
pycparser==3.0
Pygments==2.20.0
PySocks==1.7.1
pytest==9.0.3
pytest-html==4.2.0
pytest-metadata==3.1.1
python-dotenv==1.2.2
requests==2.34.2
selenium==4.44.0
sniffio==1.3.1
sortedcontainers==2.4.0
trio==0.33.0
trio-websocket==0.12.2
typing_extensions==4.15.0
urllib3==2.7.0
webdriver-manager==4.1.1
websocket-client==1.9.0
wsproto==1.3.2
```
