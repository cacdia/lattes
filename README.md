# Análise de Currículos Lattes

## 📋 Conteúdo

- [Sobre o Projeto](#-sobre-o-projeto)
- [Equipe](#-equipe)
- [Metodologia](#-metodologia)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Primeiros Passos](#-primeiros-passos)
- [Análises Realizadas](#-análises-realizadas)
- [Resultados Principais](#-resultados-principais)
- [Solução de Problemas no Windows](#-solução-de-problemas-no-windows)

## 📖 Sobre o Projeto

Este projeto de Ciência de Dados realiza uma análise abrangente dos currículos da Plataforma Lattes de docentes e pesquisadores do Centro de Informática (CI). A Plataforma Lattes, mantida pelo CNPq, é uma base de dados rica em informações sobre a produção acadêmica, profissional e intelectual de pesquisadores brasileiros.

### Objetivos Principais

- **Mapear perfis de pesquisadores**: extração e análise de dados de identificação, formação acadêmica, produções científicas e redes de colaboração
- **Explorar padrões temporais**: investigação da evolução da produção acadêmica ao longo do tempo
- **Identificar estruturas de colaboração**: análise de coautorias e projetos colaborativos entre pesquisadores
- **Investigar fatores de produtividade**: relação entre formação, experiência e produção científica
- **Descobrir agrupamentos temáticos**: clustering de pesquisadores baseado em títulos de publicações

## 👥 Equipe

- **Sarah Fernanda Calixto de Araújo** — `20240011267`
- **Luiz Carlos Veloso de Araujo Lima Neto** — `20240102334`
- **Sofia Pontes Leitão de Lima** — `20240011285`
- **Cauã Henrique Formiga de Lacerda** — `20240011089`

## 🔬 Metodologia

### 1. Coleta de Dados (Web Scraping)
Utilizamos a biblioteca **Playwright** para navegar automaticamente na Plataforma Lattes, capturando os currículos completos dos pesquisadores. Esta abordagem permite contornar limitações de APIs e capturar dados estruturados diretamente das páginas web.

### 2. Extração e Estruturação (Parsing)
Os HTMLs coletados são processados com **BeautifulSoup** para extrair informações estruturadas:
- Dados de identificação (nome, resumo, formação)
- Produções bibliográficas (artigos, livros, conferências)
- Projetos de pesquisa e extensão
- Redes de colaboração (coautores e integrantes de projetos)

### 3. Análise e Modelagem
Aplicamos técnicas de:
- **Análise de Redes**: construção de grafos de coautoria com métricas de centralidade
- **Clustering**: agrupamento temático usando TF-IDF e K-Means
- **Análise Estatística**: correlações entre formação, experiência e produtividade
- **Visualização Interativa**: uso de Plotly e NetworkX para exploração visual dos dados

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

## 🔧 Pré-requisitos

- **Python 3.13+**
- **uv** (gerenciador de pacotes e ambientes Python)
- **Git**

### Instalação do uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv
```

## 🚀 Primeiros Passos

### 1. Clone o repositório

```bash
git clone https://github.com/cacdia/lattes.git
cd lattes
```

### 2. Configure o ambiente

```bash
# Cria o ambiente virtual e instala todas as dependências
uv sync
```

### 3. Execute a coleta de dados

```bash
# Download dos currículos HTML
uv run scripts/download_profile.py --input data/professores_ci.csv

# Parsing dos HTMLs para estruturar os dados
uv run scripts/parse_profiles.py --input professores_perfil_html --output data/professores.json
```

### 4. Execute as análises

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

### 4. Clustering Temático
- **Agrupamento de publicações por similaridade de títulos**
- **Uso de TF-IDF e K-Means com validação por múltiplas métricas**
- **Visualização 2D e 3D dos clusters com PCA**
- **Identificação de áreas temáticas de pesquisa**

### 5. Análise Temporal
- **Evolução da produção científica ao longo dos anos**
- **Padrões de colaboração por período**
- **Tendências por laboratório e área de pesquisa**

## 🎯 Resultados Principais

### Produtividade Acadêmica
- **Liliane dos Santos Machado** lidera com 498 publicações e 316 coautores
- Forte correlação entre produção e colaboração (r=0.85)
- Concentração significativa: top 10% respondem por >50% das publicações

### Impacto da Formação
- Pesquisadores com **Pós-doutorado**: média de 89.7 publicações
- Pesquisadores com **Doutorado**: média de 60.1 publicações
- Pesquisadores com **Mestrado**: média de 44.3 publicações
- ANOVA confirma diferenças significativas (p < 0.001)

### Redes de Colaboração
- **67 pesquisadores** analisados com redes de coautoria bem conectadas
- Laboratórios ARIA e LAVID mostram colaboração intensa
- Identificação de "brokers" que conectam diferentes grupos de pesquisa

### Agrupamentos Temáticos
- **4 clusters principais** identificados nos títulos das publicações
- Áreas dominantes: Inteligência Artificial, Redes/Sistemas, Educação Tecnológica, Otimização
- Alta coesão interna dos clusters (Silhouette Score = 0.31)

## 🪟 Solução de Problemas no Windows

Caso encontre problemas de permissão ao executar scripts no PowerShell (comum ao instalar o uv), execute o seguinte comando para permitir a execução de scripts assinados:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Introdução à Ciência de Dados, ministrada pelo professor Yuri Malheiros.

---

**Nota**: Para reproduzir completamente as análises, execute primeiro os scripts de coleta e parsing, depois abra os notebooks na ordem sugerida. O processamento completo pode levar algumas horas dependendo do número de currículos.
