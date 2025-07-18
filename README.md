# Configuração de Pre-commit com Ruff

Este guia descreve como configurar o `pre-commit` com o `Ruff` neste repositório. O objetivo é garantir a qualidade e a formatação do código Python de forma automática antes de cada commit, usando uma ferramenta moderna e extremamente rápida.

## O que é o Pre-commit?

`pre-commit` é um framework para gerenciar e manter hooks de Git multi-linguagem. Antes que seu código seja enviado com um `git commit`, ele executa scripts pré-configurados (hooks) para verificar e corrigir seu código, garantindo que os padrões do projeto sejam seguidos.

## O que é o Ruff?

`Ruff` é um linter e formatador de código Python extremamente rápido, escrito em Rust. Ele pode substituir dezenas de ferramentas como Flake8, isort, pyupgrade e Black.

---

## Guia de Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

### Passo 1: Instalar a ferramenta `pre-commit`

Primeiro, você precisa ter o pacote `pre-commit` instalado no seu ambiente Python.

* **Usando `pip`:**

    ```bash
    pip install pre-commit
    ```

* **Usando `uv` (recomendado para este projeto):**

    ```bash
    uv pip install pre-commit
    ```

Para verificar se a instalação foi bem-sucedida, rode:

```bash
pre-commit --version
```


### Passo 2: Criar o arquivo de configuração `.pre-commit-config.yaml`

O `pre-commit` é configurado por um arquivo na raiz do repositório.



* **Crie um arquivo chamado `.pre-commit-config.yaml` na raiz do seu projeto.**

  Copie e cole o seguinte conteúdo dentro dele:

    ```yaml
    # .pre-commit-config.yaml
    repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.12.4
    hooks:
      # Run the linter.
      - id: ruff-check
        args: [ --fix ]
      # Run the formatter.
      - id: ruff-format
    ```

### Passo 3: Instalar os hooks no Git

O último passo é instalar os hooks no seu repositório Git local. Este comando lê o seu arquivo de configuração e configura o script que será executado antes de cada commit.

Execute o seguinte comando na raiz do projeto:

```bash
pre-commit install
```
Você deverá ver a mensagem: `pre-commit installed at .git/hooks/pre-commit`.

Pronto! A partir de agora, o pre-commit será executado automaticamente a cada git commit, garantindo a qualidade e o padrão do seu código.
