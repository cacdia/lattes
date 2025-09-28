# Análise de Currículos Lattes

## 📋 Conteúdo

- [Sobre o Projeto](#-sobre-o-projeto)
- [Equipe](#-equipe)
- [Metodologia](#-metodologia)
- [Pré-requisitos](#-pré-requisitos)
- [Primeiros Passos](#-primeiros-passos)
- [Análises Realizadas](#-análises-realizadas)
- [Resultados Principais](#-resultados-principais)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Solução de Problemas no Windows](#-solução-de-problemas-no-windows)

## 📖 Sobre o Projeto

Este projeto de Ciência de Dados realiza uma análise abrangente dos currículos da Plataforma Lattes de docentes e pesquisadores do Centro de Informática (CI). A Plataforma Lattes, mantida pelo CNPq, é uma base de dados rica em informações sobre a produção acadêmica, profissional e intelectual de pesquisadores brasileiros.

## 👥 Equipe

- **Sarah Fernanda Calixto de Araújo** — `20240011267`
- **Luiz Carlos Veloso de Araujo Lima Neto** — `20240102334`
- **Sofia Pontes Leitão de Lima** — `20240011285`
- **Cauã Henrique Formiga de Lacerda** — `20240011089`

## 🔬 Metodologia

### 1. Coleta de Dados (Web Scraping)
Utilizamos a biblioteca **Playwright** para navegar automaticamente na Plataforma Lattes, capturando os currículos completos dos pesquisadores. Esta abordagem permite contornar limitações de APIs e capturar dados estruturados diretamente das páginas web.

### 2. Extração e Estruturação (Parsing)
Após o download, um segundo script utiliza as bibliotecas **BeautifulSoup** e **Pandas** para fazer o parsing do conteúdo HTML. Ele extrai informações-chave como dados básicos (nome, resumo), formação acadêmica, projetos de pesquisa e redes de colaboração (coautores e integrantes de projetos). Os dados são então consolidados e exportados em formatos estruturados como JSON, prontos para a análise.

### 3. Análise e Modelagem
Aplicamos técnicas de:
- **Análise de Redes**: construção de grafos de coautoria com métricas de centralidade
- **Clustering**: agrupamento temático usando TF-IDF e K-Means
- **Análise Estatística**: correlações entre formação, experiência e produtividade
- **Visualização Interativa**: uso de Plotly e NetworkX para exploração visual dos dados

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

### Execute as análises

Abra o Jupyter Lab e execute os notebooks na pasta `notebook/`:

```bash
uv run jupyter lab notebook/
```

Comece pelo [`notebook_relatorio.ipynb`](notebook/notebook_relatorio.ipynb) que contém as análises principais.

## 📊 Análises Realizadas

### 1. Ranking de Produtividade
- **Top pesquisadores por número de publicações**
- **Top pesquisadores por número de coautorias**
- **Análise de correlação entre produção e colaboração**

### 2. Impacto da Formação
- **Relação entre nível de formação (Mestrado/Doutorado/Pós-doc) e produtividade**
- **Análise estatística com ANOVA e tratamento de outliers**
- **Correlação entre anos de experiência e produção científica**

### 3. Análise de Redes de Colaboração
- **Construção de grafos de coautoria**
- **Métricas de centralidade (betweenness, eigenvector, grau)**
- **Visualização interativa com Plotly**
- **Análise específica dos laboratórios ARIA e LAVID**

### 4. Análise de Redes de Coautoria entre Docentes do CI
- **Construção de grafo não direcionado com nós = pesquisadores**
- **Arestas ponderadas pelo número de publicações em coautoria**
- **Cálculo de métricas de centralidade (betweenness, eigenvector, grau)**
- **Filtragem para coautorias internas (apenas entre docentes do CI)**
- **Visualização interativa com layout forçado e cores por centralidade**
- **Análise específica de subrede ARIA/LAVID com mapeamento por laboratório**

### 5. Clustering Temático de Títulos de Publicações
- **Pré-processamento de texto com remoção de stopwords em português**
- **Vetorização TF-IDF de títulos de publicações (3.000 features)**
- **Determinação do número ótimo de clusters usando múltiplas métricas**:
  - Método do Cotovelo (WCSS)
  - Coeficiente de Silhueta
  - Índice Calinski-Harabasz
  - Índice Davies-Bouldin
- **Aplicação de K-Means com validação por ranking combinado**
- **Visualização 2D e 3D dos clusters usando PCA**
- **Identificação de 4 clusters principais de áreas temáticas**

## 📁 Estrutura do Projeto

```
lattes/
├── .github/
│   └── ISSUE_TEMPLATE/
├── data/
│   ├── professores_ci.csv          # Lista de entrada dos professores
│   ├── professores.json            # Dados consolidados (JSON)
│   ├── prof_labs.csv               # Mapeamento professor ↔ laboratório
│   └── titulos_producoes.json      # Títulos para análise de clustering
├── professores_perfil_html/        # HTMLs dos currículos coletados
├── notebook/
│   ├── notebook_relatorio.ipynb    # Notebook principal com análises
│   ├── analysis.ipynb              # Análises exploratórias adicionais
│   ├── laboratorios.ipynb          # Análises por laboratório
│   ├── proximidade_titulos.ipynb   # Análise de similaridade de títulos
│   └── utils_lattes.py             # Funções utilitárias
├── scripts/
│   ├── download_profile.py         # Script para coleta dos currículos
│   └── parse_profiles.py           # Script para parsing dos HTMLs
├── src/
│   └── __init__.py
├── .vscode/                        # Configurações do VS Code
├── .gitignore
├── pyproject.toml                  # Dependências e metadados
├── README.md
├── ruff.toml                       # Configurações de formatação
└── uv.lock                         # Lock file para dependências
```

## 🪟 Solução de Problemas no Windows

Caso encontre problemas de permissão ao executar scripts no PowerShell (comum ao instalar o uv), execute o seguinte comando para permitir a execução de scripts assinados:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Introdução à Ciência de Dados, ministrada pelo professor Yuri Malheiros.

---

**Nota**: Para reproduzir completamente as análises, execute primeiro os scripts de coleta e parsing, depois abra os notebooks na ordem sugerida.
