import os
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
import argparse


def _obter_nomes_de_citacao_do_pesquisador(soup):
    """
    Encontra o campo "Nome em citações bibliográficas" e extrai todas as variações
    de nome que o pesquisador usa em publicações.

    Isso é importante para que o script não liste o próprio pesquisador como um coautor.

    Args:
        soup (BeautifulSoup): O objeto BeautifulSoup com o HTML do currículo.

    Returns:
        set: Um conjunto com os nomes de citação em maiúsculas.
    """
    nomes_de_citacao = set()
    cabecalho_citacoes = soup.find("b", string="Nome em citações bibliográficas")
    if cabecalho_citacoes:
        div_pai = cabecalho_citacoes.find_parent("div")
        div_com_os_nomes = div_pai.find_next_sibling("div")
        if div_com_os_nomes:
            texto_dos_nomes = div_com_os_nomes.get_text(separator=" ", strip=True)
            lista_de_nomes = texto_dos_nomes.split(";")
            for nome in lista_de_nomes:
                nome_limpo = nome.strip()
                if nome_limpo:
                    nomes_de_citacao.add(nome_limpo.upper())
    return nomes_de_citacao


def _extrair_coautores(soup, nomes_de_citacao_do_pesquisador):
    """
    Extrai os nomes dos coautores a partir da seção de produção bibliográfica.

    Args:
        soup (BeautifulSoup): O objeto com o HTML do currículo.
        nomes_de_citacao_do_pesquisador (set): Nomes do dono do perfil para filtrar.

    Returns:
        list: Uma lista ordenada com os nomes dos coautores.
    """
    coautores = set()
    ancora_producao = soup.find("a", attrs={"name": "ProducaoBibliografica"})
    if not ancora_producao:
        return []
    container_geral = ancora_producao.find_parent("div", class_="title-wrapper")
    itens_publicacao = container_geral.find_all("div", class_="layout-cell-11")
    for item in itens_publicacao:
        if not item.find("span", class_="transform"):
            continue
        texto_completo = item.get_text(separator=" ", strip=True)
        texto_sem_numero = re.sub(r"^\d+\.\s*", "", texto_completo).strip()
        partes = texto_sem_numero.split(" . ")
        if len(partes) < 2:
            continue
        texto_dos_autores = partes[0]
        lista_de_autores = texto_dos_autores.split(";")
        for autor in lista_de_autores:
            autor_limpo = re.sub(r"</?b>", "", autor).strip()
            e_nome_valido = autor_limpo and len(autor_limpo) < 70
            e_coautor = autor_limpo.upper() not in nomes_de_citacao_do_pesquisador
            if e_nome_valido and e_coautor:
                coautores.add(autor_limpo)
    return sorted(list(coautores))


def _extrair_colaboradores_projetos(soup, nome_do_pesquisador):
    """
    Extrai os nomes dos colaboradores a partir da seção de projetos de pesquisa.

    Args:
        soup (BeautifulSoup): O objeto com o HTML do currículo.
        nome_do_pesquisador (str): Nome do dono do perfil para filtrar.

    Returns:
        list: Uma lista ordenada com os nomes dos colaboradores.
    """
    colaboradores = set()
    ancora_projetos = soup.find("a", attrs={"name": "ProjetosPesquisa"})
    if not ancora_projetos:
        return []
    container_de_dados = ancora_projetos.find_parent(
        "div", class_="title-wrapper"
    ).find_next("div", class_="layout-cell-12")
    if not container_de_dados:
        return []
    itens_de_projeto = container_de_dados.find_all("div", class_="layout-cell-9")
    for item in itens_de_projeto:
        texto_do_item = item.get_text(separator="|", strip=True)
        match = re.search(r"Integrantes:\s*([^|]+)", texto_do_item)
        if match:
            texto_dos_colaboradores = match.group(1).strip().replace(".", "")
            lista_de_colaboradores = texto_dos_colaboradores.split("/")
            for colaborador in lista_de_colaboradores:
                nome = colaborador.split(" - ")[0].strip()
                if nome and nome.lower() != nome_do_pesquisador.lower():
                    colaboradores.add(nome)
    return sorted(list(colaboradores))


def _extrair_dados_basicos(soup):
    """
    Extrai o nome e o resumo do pesquisador.
    """
    try:
        nome = soup.find("h2", class_="nome").text.strip()
    except AttributeError:
        nome = "Nome não encontrado"
    try:
        resumo_tag = soup.find("p", class_="resumo")
        resumo = re.sub(
            r"\s*\((?:Texto informado pelo autor)\)\s*$",
            "",
            resumo_tag.get_text(strip=True),
            flags=re.IGNORECASE,
        )
    except AttributeError:
        resumo = ""
    return {"nome": nome, "resumo": resumo}


def _extrair_formacao(soup):
    formacoes = []
    ancora_formacao = soup.find("a", attrs={"name": "FormacaoAcademicaTitulacao"})
    if not ancora_formacao:
        return formacoes
    container_div = ancora_formacao.find_next("div", class_="layout-cell-12")
    if not container_div:
        return formacoes
    itens_periodo = container_div.find_all(
        "div", class_="layout-cell-3", recursive=False
    )
    for div_periodo in itens_periodo:
        div_descricao = div_periodo.find_next_sibling("div", class_="layout-cell-9")
        if not div_descricao:
            continue
        tooltip_oasis = div_descricao.find("a", class_="tooltip-oasis")
        if tooltip_oasis:
            tooltip_oasis.decompose()
        descricao_completa = " ".join(div_descricao.text.split())
        tipo = "Não identificado"
        if "Doutorado" in descricao_completa:
            tipo = "Doutorado"
        elif "Mestrado" in descricao_completa:
            tipo = "Mestrado"
        elif "Especialização" in descricao_completa:
            tipo = "Especialização"
        elif "Graduação" in descricao_completa:
            tipo = "Graduação"
        elif (
            "Pós-Doutorado" in descricao_completa
            or "Pós-doutorado" in descricao_completa
        ):
            tipo = "Pós-doutorado"
        elif "Aperfeiçoamento" in descricao_completa:
            tipo = "Aperfeiçoamento"
        elif "Curso técnico/profissionalizante" in descricao_completa:
            tipo = "Técnico/Profissionalizante"
        dados_da_formacao = {
            "periodo": " ".join(div_periodo.text.split()),
            "tipo_formacao": tipo,
            "descricao_formacao": descricao_completa,
        }
        formacoes.append(dados_da_formacao)
    return formacoes


def _extrair_projetos(soup):
    """
    Extrai os projetos de pesquisa ou extensão.
    """
    projetos = []
    ancora_projetos = soup.find("a", attrs={"name": "ProjetosPesquisa"})
    if not ancora_projetos:
        ancora_projetos = soup.find("a", attrs={"name": "ProjetosExtensao"})
        if not ancora_projetos:
            return projetos
    container_de_dados = ancora_projetos.find_parent(
        "div", class_="title-wrapper"
    ).find_next("div", class_="layout-cell-12")
    if not container_de_dados:
        return projetos
    divs_periodo = container_de_dados.find_all("div", class_="layout-cell-3")
    divs_descricao = container_de_dados.find_all("div", class_="layout-cell-9")
    for div_periodo, div_info in zip(divs_periodo, divs_descricao):
        linhas_de_info = [s.strip() for s in div_info.stripped_strings]
        titulo_do_projeto = (
            linhas_de_info[0] if linhas_de_info else "Título não encontrado"
        )
        if titulo_do_projeto.startswith("Periódico:") or titulo_do_projeto.startswith(
            "Grande área:"
        ):
            continue
        descricao_completa = " ".join(linhas_de_info)
        situacao_match = re.search(r"Situação:\s*([^;]+);", descricao_completa)
        natureza_match = re.search(r"Natureza:\s*([^.]+)\.", descricao_completa)
        dados_do_projeto = {
            "periodo_projeto": " ".join(div_periodo.text.split()),
            "titulo_projeto": titulo_do_projeto,
            "situacao_projeto": situacao_match.group(1).strip()
            if situacao_match
            else None,
            "natureza_projeto": natureza_match.group(1).strip()
            if natureza_match
            else None,
        }
        projetos.append(dados_do_projeto)
    return projetos


def extrair_dados_professor(conteudo_html):
    """
    Função principal que orquestra a extração de todos os dados de um currículo.
    """
    soup = BeautifulSoup(conteudo_html, "lxml")
    try:
        dados_extraidos = _extrair_dados_basicos(soup)
        nome_do_pesquisador = dados_extraidos.get("nome", "")
        nomes_de_citacao = _obter_nomes_de_citacao_do_pesquisador(soup)
        if nome_do_pesquisador:
            partes_nome = nome_do_pesquisador.split()
            if len(partes_nome) > 1:
                formato_citacao = f"{partes_nome[-1].upper()}, {' '.join(p[0].upper() + '.' for p in partes_nome[:-1])}"
                nomes_de_citacao.add(formato_citacao)
        dados_extraidos["formacao"] = _extrair_formacao(soup)
        dados_extraidos["projetos_pesquisa"] = _extrair_projetos(soup)
        dados_extraidos["coautores_publicacoes"] = _extrair_coautores(
            soup, nomes_de_citacao
        )
        dados_extraidos["colaboradores_projetos"] = _extrair_colaboradores_projetos(
            soup, nome_do_pesquisador
        )
        return dados_extraidos
    except Exception as e:
        print(f"Aviso: Erro inesperado ao extrair dados: {e}")
        return {}


def consolidar_dados_professor_em_linha_unica(dados_extraidos):
    """
    Converte o dicionário de dados extraídos (que contém listas) em um
    dicionário simples, onde cada campo é uma string, para representar uma única linha no CSV/JSON.
    """
    linha_unica = {
        "nome_professor": dados_extraidos.get("nome"),
        "resumo_professor": dados_extraidos.get("resumo"),
    }
    lista_de_formacoes = dados_extraidos.get("formacao", [])
    lista_de_strings_formacao = []
    for formacao in lista_de_formacoes:
        texto_formatado = f"{formacao.get('tipo_formacao', '')} ({formacao.get('periodo', '')}): {formacao.get('descricao_formacao', '')}"
        lista_de_strings_formacao.append(texto_formatado)
    linha_unica["formacoes_academicas"] = " | ".join(lista_de_strings_formacao)
    lista_de_projetos = dados_extraidos.get("projetos_pesquisa", [])
    lista_de_strings_projetos = []
    for projeto in lista_de_projetos:
        texto_formatado = f"{projeto.get('titulo_projeto', '')} ({projeto.get('periodo_projeto', '')}) - Situação: {projeto.get('situacao_projeto', 'N/A')}"
        lista_de_strings_projetos.append(texto_formatado)
    linha_unica["projetos_pesquisa"] = " | ".join(lista_de_strings_projetos)
    linha_unica["coautores_publicacoes"] = "; ".join(
        dados_extraidos.get("coautores_publicacoes", [])
    )
    linha_unica["colaboradores_projetos"] = "; ".join(
        dados_extraidos.get("colaboradores_projetos", [])
    )
    return linha_unica


def processar_diretorio(diretorio_de_entrada):
    """
    Lê todos os arquivos .html de um diretório, extrai os dados de cada um,
    e retorna um DataFrame do Pandas com todos os dados consolidados.
    """
    arquivos_html = [f for f in os.listdir(diretorio_de_entrada) if f.endswith(".html")]
    print(
        f"Iniciando o processamento de {len(arquivos_html)} arquivos HTML de '{diretorio_de_entrada}'..."
    )
    dados_consolidados = []
    for i, nome_arquivo in enumerate(arquivos_html):
        caminho_completo = os.path.join(diretorio_de_entrada, nome_arquivo)
        print(f"  ({i + 1}/{len(arquivos_html)}) Processando: {nome_arquivo}")
        with open(caminho_completo, encoding="utf-8") as arquivo:
            conteudo_html = arquivo.read()
        dados_extraidos = extrair_dados_professor(conteudo_html)
        if dados_extraidos and dados_extraidos.get("nome"):
            linha_unica = consolidar_dados_professor_em_linha_unica(dados_extraidos)
            dados_consolidados.append(linha_unica)
        else:
            print(
                f"    -> Aviso: Nenhum dado extraído de {nome_arquivo}. O arquivo pode estar vazio ou mal formatado."
            )
    print("\nProcessamento concluído!")
    return pd.DataFrame(dados_consolidados)


def main():
    """
    Função principal que gerencia a execução do script:
    - Lê os argumentos da linha de comando (--input e --output).
    - Chama a função de processamento.
    - Salva o resultado no formato desejado (CSV ou JSON).
    """
    parser = argparse.ArgumentParser(
        description="Processa currículos Lattes em HTML. Salva em CSV ou JSON, inferindo pelo nome do arquivo de saída."
    )
    parser.add_argument(
        "--input", required=True, help="Diretório contendo os arquivos HTML de entrada."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do arquivo de saída. Ex: 'dados.csv' ou 'dados.json'.",
    )
    args = parser.parse_args()
    if not os.path.isdir(args.input):
        print(f"Erro: O diretório de entrada '{args.input}' não é válido.")
        return
    dataframe_final = processar_diretorio(args.input)
    if dataframe_final.empty:
        print("Nenhum dado foi extraído para ser salvo.")
        return
    caminho_de_saida = args.output
    diretorio_de_saida = os.path.dirname(caminho_de_saida)
    if diretorio_de_saida:
        os.makedirs(diretorio_de_saida, exist_ok=True)
    _raiz, extensao = os.path.splitext(caminho_de_saida)
    extensao = extensao.lower()
    try:
        if extensao == ".json":
            print("\nFormato de saída detectado: JSON")
            dados_em_formato_json = dataframe_final.to_dict(orient="records")
            with open(caminho_de_saida, "w", encoding="utf-8") as arquivo_json:
                json.dump(
                    dados_em_formato_json, arquivo_json, ensure_ascii=False, indent=4
                )
        elif extensao == ".csv":
            print("\nFormato de saída detectado: CSV")
            dataframe_final.to_csv(caminho_de_saida, index=False, encoding="utf-8-sig")
        else:
            print(
                f"\nAviso: Extensão '{extensao}' não é suportada. Use '.csv' ou '.json'."
            )
            print("Nenhum arquivo foi salvo.")
            return
        print(f"Dados consolidados foram salvos com sucesso em '{caminho_de_saida}'")
        print(f"Total de {len(dataframe_final)} professores processados.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")


if __name__ == "__main__":
    main()
