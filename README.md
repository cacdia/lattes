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

### 1\. Coleta de Dados (Scraping)
Utilizamos a biblioteca Playwright para navegar e interagir com a plataforma, permitindo a captura de todos os currículos de interesse. Posteriormente, realizamos um parsing do HTML coletado para extrair as seções relevantes e preparar os dados para análise.

### 2\. Extração e Estruturação (Parsing)
Após o download, um segundo script utiliza as bibliotecas BeautifulSoup e Pandas para fazer o parsing do conteúdo HTML. Ele extrai informações-chave como dados básicos (nome, resumo), formação acadêmica, projetos de pesquisa e redes de colaboração (coautores e integrantes de projetos). Os dados são então consolidados e exportados em formatos estruturados como CSV ou JSON, prontos para a análise.

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

O projeto funciona em duas etapas principais: primeiro baixar os currículos, depois processá-los.

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

Após baixar os arquivos HTML, utilize o script parse_lattes.py para processá-los e gerar um arquivo consolidado com os dados extraídos.

O formato de saída (CSV ou JSON) é definido pela extensão do arquivo que você especificar em --output.

#### Exemplo para saída em CSV:

```bash
# Processa os HTMLs da pasta 'meus_curriculos' e salva os dados em um arquivo CSV
uv run scripts/parse_profiles.py --input meu_diretorio --output data/professores.csv
```

#### Exemplo para saída em JSON:

```bash
# Processa os HTMLs e salva os dados em formato JSON
uv run scripts/parse_profiles.py --input meu_diretorio --output data/professores.json
```

## 📁 Estrutura do Projeto

```
lattes/
├── .github/
├── data/
│   └── professores_ci.csv    # Arquivo de entrada com os dados dos professores
├── scripts/
│   ├── download_profile.py   # Script para baixar os currículos em HTML
│   └── parse_profiles.py       # Script para extrair dados dos arquivos HTML
├── src/
│   └── __init__.py
├── .vscode/
├── .gitignore
├── pyproject.toml            # Metadados e dependências do projeto
├── README.md                 # Este arquivo
├── ruff.toml                 # Configurações do linter e formatador
└── uv.lock                   # Arquivo de lock para instalações consistentes
```


## 🪟 Solução de Problemas no Windows

Caso encontre problemas de permissão ao executar scripts no PowerShell (comum ao instalar o `uv`), execute o seguinte comando para permitir a execução de scripts assinados:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

-----
