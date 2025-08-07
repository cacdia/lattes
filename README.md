# Análise de Currículos Lattes

## 📋 Conteúdo

- [Sobre o Projeto](#-sobre-o-projeto)
- [Equipe](#-equipe)
- [Metodologia](#-metodologia)
- [Pré-requisitos](#-pré-requisitos)
- [Primeiros Passos](#-primeiros-passos)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Solução de Problemas no Windows](#-solução-de-problemas-no-windows)


## 📖 Sobre o Projeto
Este projeto de Ciência de Dados tem como objetivo principal extrair, limpar e analisar dados provenientes dos currículos da Plataforma Lattes. A Plataforma Lattes, mantida pelo CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico), é uma base de dados rica em informações sobre a produção acadêmica, profissional e intelectual de pesquisadores brasileiros.

## 👥 Equipe

  - Sarah Fernanda Calixto de Araújo - `20240011267`
  - Luiz Carlos Veloso de Araujo Lima Neto - `20240102334`
  - Sofia Pontes Leitão de Lima - `20240011285`
  - Cauã Henrique Formiga de Lacerda - `20240011089`

## 🔬 Metodologia

### Coleta de Dados
Utilizamos a biblioteca Playwright para navegar e interagir com a plataforma, permitindo a captura de todos os currículos de interesse. Posteriormente, realizamos um parsing do HTML coletado para extrair as seções relevantes e preparar os dados para análise.


## 🔧 Pré-requisitos

Certifique-se de instalar os seguintes programas antes de começar:

- **Visual Studio Code** 👉 [Download VSCode](https://code.visualstudio.com/)

- **Git** 👉 [Download Git](https://git-scm.com/downloads)

- **uv** O `uv` é um gerenciador de pacotes e ambientes virtuais extremamente rápido para Python. Instale utilizando o comando adequado ao seu sistema operacional:

  ```bash
  # Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

  # macOS/Linux
  curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh


## 🚀 Primeiros Passos

Siga os passos abaixo para configurar rapidamente o projeto em sua máquina.

### 1\. Clone o repositório

```bash
git clone https://github.com/cacdia/lattes.git
cd lattes
```

### 2\. Configure o ambiente virtual

Crie o ambiente virtual e instale todas as dependências do projeto com um único comando:

```bash
# Sincroniza o ambiente: cria o .venv e instala os pacotes listados no pyproject.toml
uv sync
```

### 3\. Configure o VSCode

Abra o projeto no Visual Studio Code:

```bash
code .
```

#### Instale as extensões recomendadas

Ao abrir o projeto pela primeira vez:

- Uma notificação aparecerá sugerindo a instalação das extensões recomendadas.
- Clique em **Install All** ou em **Show Recommendations**.
- Alternativamente, pressione `Ctrl+Shift+X` (ou `Cmd+Shift+X` no macOS) e digite `@recommended` na barra de pesquisa.

#### Selecione o interpretador Python correto

É crucial que o VSCode utilize o ambiente virtual (`.venv`) que o `uv` criou.

1.  Pressione `F1` (ou `Ctrl+Shift+P`)
2.  Digite **Python: Select Interpreter**
3.  Escolha o interpretador que tem **('.venv')** no nome. Ex: `"Python 3.13 ('.venv':venv)"`

### 4\. Execute o projeto

O principal script do projeto realiza o download dos currículos Lattes listados em um arquivo CSV.

```bash
# Comando principal para executar o download
uv run scripts/download_profile.py --input data/professores_ci.csv
```

#### Exemplo com diretório de saída personalizado

Você também pode especificar onde os arquivos HTML dos currículos serão salvos com a flag `--output`.

```bash
# Salva os arquivos no diretório 'meu_diretorio'
uv run scripts/download_profile.py --input data/professores_ci.csv --output meu_diretorio
```

## 📁 Estrutura do Projeto

```
lattes/
├── .github/              # Arquivos de configuração do GitHub
├── data/
│   └── professores_ci.csv  # Arquivo de entrada com os dados dos professores
├── scripts/
│   └── download_profile.py # Script principal para baixar os currículos
├── src/
│   └── __init__.py         # Define o diretório como um pacote Python
├── .vscode/              # Configurações recomendadas para o VS Code
├── .gitignore            # Arquivos e pastas a serem ignorados pelo Git
├── pyproject.toml        # Metadados e dependências do projeto (gerenciado pelo uv)
├── ruff.toml             # Configurações do linter e formatador Ruff
└── uv.lock               # Arquivo de lock para garantir instalações consistentes
```


## 🪟 Solução de Problemas no Windows

Caso encontre problemas de permissão ao executar scripts no PowerShell (comum ao instalar o `uv`), execute o seguinte comando para permitir a execução de scripts assinados:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

-----



