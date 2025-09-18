import argparse
import json
import logging
import os
import re
from dataclasses import dataclass, asdict, field
from bs4 import BeautifulSoup, Tag

# Configure logging for debugging and error tracking
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class Identificacao:
    nome: str
    nomes_citacao: list[str]
    lattes_id: str
    pais_nacionalidade: str
    orcid_id: str | None = None


@dataclass
class Endereco:
    endereco_profissional: str


@dataclass
class Formacao:
    periodo: str
    tipo_formacao: str
    descricao_formacao: str
    titulo: str | None = None
    orientador: str | None = None
    bolsa: str | None = None


@dataclass
class PosDoutorado:
    periodo: str
    descricao: str


@dataclass
class FormacaoComplementar:
    periodo: str
    descricao: str


@dataclass
class AtividadeProfissional:
    periodo: str
    descricao: str
    cargo_funcao: str | None = None
    disciplinas_ministradas: list[str] = field(default_factory=list)
    linhas_pesquisa: list[str] = field(default_factory=list)


@dataclass
class VinculoInstitucional:
    instituicao: str
    periodo: str
    vinculo: str
    enquadramento: str
    carga_horaria: str | None = None
    regime: str | None = None
    atividades: list[AtividadeProfissional] = field(default_factory=list)


@dataclass
class Projeto:
    periodo: str
    titulo: str
    situacao: str | None = None
    natureza: str | None = None
    integrantes: list[str] = field(default_factory=list)


@dataclass
class ProducaoBibliografica:
    titulo: str
    autores: list[str]
    ano: str | None = None
    revista: str | None = None
    doi: str | None = None
    paginas: str | None = None


@dataclass
class ProfessorData:
    identificacao: Identificacao
    endereco: Endereco
    resumo: str
    formacao_academica: list[Formacao]
    pos_doutorado: list[PosDoutorado]
    formacao_complementar: list[FormacaoComplementar]
    atuacao_profissional: list[VinculoInstitucional]
    projetos_pesquisa: list[Projeto]
    projetos_extensao: list[Projeto]
    producao_bibliografica: list[ProducaoBibliografica]
    coautores_publicacoes: list[str]
    colaboradores_projetos: list[str]


def _extract_text_from_tag(
    tag: Tag | None, separator: str = " ", strip: bool = True
) -> str:
    """
    Safely extracts text from a BeautifulSoup Tag, handling None cases and type mismatches.

    Args:
        tag (Tag | None): The BeautifulSoup tag to extract text from.
        separator (str): Separator for joining text elements. Defaults to " ".
        strip (bool): Whether to strip whitespace. Defaults to True.

    Returns:
        str: Extracted text or empty string if tag is None or invalid.
    """
    if tag is None or not isinstance(tag, Tag):
        return ""
    return tag.get_text(separator=separator, strip=strip)


def _find_anchor_and_container(
    soup: BeautifulSoup, anchor_name: str, container_class: str
) -> Tag | None:
    """
    Finds the container div following a specific anchor in the HTML, with type safety.

    Args:
        soup (BeautifulSoup): The parsed HTML.
        anchor_name (str): The name attribute of the anchor tag.
        container_class (str): The class of the container div.

    Returns:
        Tag | None: The container div or None if not found.
    """
    anchor = soup.find("a", attrs={"name": anchor_name})
    if anchor is None or not isinstance(anchor, Tag):
        return None
    parent_div = anchor.find_parent("div", class_="title-wrapper")
    if parent_div is None or not isinstance(parent_div, Tag):
        return None
    container = parent_div.find_next("div", class_=container_class)
    return container if isinstance(container, Tag) else None


def _extract_names_in_citations(soup: BeautifulSoup) -> set[str]:
    """
    Extracts unique citation names from the "Nome em citações bibliográficas" section.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        set[str]: A set of uppercase citation names.
    """
    names: set[str] = set()
    header = soup.find(
        "b",
        string=lambda text: bool(text and "Nome em citações bibliográficas" in text),
    )
    if header is None or not isinstance(header, Tag):
        return names
    parent_div = header.find_parent("div", class_="layout-cell-pad-5")
    if parent_div is None or not isinstance(parent_div, Tag):
        return names
    grandparent = parent_div.find_parent("div", class_="layout-cell")
    if grandparent is None or not isinstance(grandparent, Tag):
        return names
    names_div = grandparent.find_next_sibling("div", class_="layout-cell-9")
    if names_div is None or not isinstance(names_div, Tag):
        return names
    text = _extract_text_from_tag(names_div)
    for name in text.split(";"):
        cleaned_name = name.strip().upper()
        if cleaned_name:
            names.add(cleaned_name)
    return names


def _extract_coauthors(soup: BeautifulSoup, citation_names: set[str]) -> list[str]:
    """
    Extracts co-authors from the production section, filtering out the profile owner's names.

    Args:
        soup (BeautifulSoup): The parsed HTML.
        citation_names (set[str]): Names to filter out.

    Returns:
        list[str]: Sorted list of unique co-authors.
    """
    coauthors: set[str] = set()
    container = _find_anchor_and_container(
        soup, "ProducaoBibliografica", "layout-cell-12"
    )
    if container is None:
        return []
    items = container.find_all("div", class_="layout-cell-11")
    for item in items:
        if not isinstance(item, Tag):
            continue
        transform_span = item.find("span", class_="transform")
        if transform_span is None:
            continue
        text = _extract_text_from_tag(item)
        text_no_number = re.sub(r"^\d+\.\s*", "", text).strip()
        parts = text_no_number.split(" . ")
        if len(parts) < 2:
            continue
        authors_text = parts[0]
        for author in authors_text.split(";"):
            cleaned_author = re.sub(r"</?b>", "", author).strip()
            if (
                cleaned_author
                and len(cleaned_author) < 70
                and cleaned_author.upper() not in citation_names
            ):
                coauthors.add(cleaned_author)
    return sorted(list(coauthors))


def _extract_project_collaborators(soup: BeautifulSoup, owner_name: str) -> list[str]:
    """
    Extracts collaborators from the projects section, filtering out the profile owner.

    Args:
        soup (BeautifulSoup): The parsed HTML.
        owner_name (str): The name of the profile owner.

    Returns:
        list[str]: Sorted list of unique collaborators.
    """
    collaborators: set[str] = set()
    container = _find_anchor_and_container(soup, "ProjetosPesquisa", "layout-cell-12")
    if container is None:
        container = _find_anchor_and_container(
            soup, "ProjetosExtensao", "layout-cell-12"
        )
    if container is None:
        return []
    items = container.find_all("div", class_="layout-cell-9")
    for item in items:
        if not isinstance(item, Tag):
            continue
        text = _extract_text_from_tag(item)
        match = re.search(r"Integrantes:\s*([^|]+)", text)
        if match:
            collaborators_text = match.group(1).strip().replace(".", "")
            for collab in collaborators_text.split("/"):
                name = collab.split(" - ")[0].strip()
                if name and name.lower() != owner_name.lower():
                    collaborators.add(name)
    return sorted(list(collaborators))


def _extract_identificacao(soup: BeautifulSoup) -> Identificacao:
    """
    Extracts identification information.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        Identificacao: Identification data.
    """
    name_tag = soup.find("h2", class_="nome")
    name = (
        _extract_text_from_tag(name_tag)
        if isinstance(name_tag, Tag)
        else "Nome não encontrado"
    )

    citation_names = list(_extract_names_in_citations(soup))

    lattes_id_span = soup.find(
        "span", attrs={"style": "font-weight: bold; color: #326C99;"}
    )
    lattes_id = ""
    if lattes_id_span and isinstance(lattes_id_span, Tag):
        lattes_id = _extract_text_from_tag(lattes_id_span)

    pais_tag = soup.find(
        "b", string=lambda text: bool(text and "País de Nacionalidade" in text)
    )
    pais = ""
    if pais_tag:
        parent_div = pais_tag.find_parent("div", class_="layout-cell-pad-5")
        if parent_div:
            grandparent = parent_div.find_parent("div", class_="layout-cell")
            if grandparent:
                next_div = grandparent.find_next_sibling("div", class_="layout-cell-9")
                if next_div and isinstance(next_div, Tag):
                    pais = _extract_text_from_tag(next_div)

    orcid_tag = soup.find("b", string=lambda text: bool(text and "Orcid iD" in text))
    orcid = None
    if orcid_tag:
        parent_div = orcid_tag.find_parent("div", class_="layout-cell-pad-5")
        if parent_div:
            grandparent = parent_div.find_parent("div", class_="layout-cell")
            if grandparent:
                next_div = grandparent.find_next_sibling("div", class_="layout-cell-9")
                if next_div and isinstance(next_div, Tag):
                    orcid_text = _extract_text_from_tag(next_div)
                    orcid_match = re.search(
                        r"https://orcid\.org/(\d{4}-\d{4}-\d{4}-\d{4})", orcid_text
                    )
                    if orcid_match:
                        orcid = orcid_match.group(1)

    return Identificacao(
        nome=name,
        nomes_citacao=citation_names,
        lattes_id=lattes_id,
        pais_nacionalidade=pais,
        orcid_id=orcid,
    )


def _extract_endereco(soup: BeautifulSoup) -> Endereco:
    """
    Extracts address information.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        Endereco: Address data.
    """
    endereco_tag = soup.find(
        "b", string=lambda text: bool(text and "Endereço Profissional" in text)
    )
    endereco = ""
    if endereco_tag:
        parent_div = endereco_tag.find_parent("div", class_="layout-cell-pad-5")
        if parent_div:
            grandparent = parent_div.find_parent("div", class_="layout-cell")
            if grandparent:
                next_div = grandparent.find_next_sibling("div", class_="layout-cell-9")
                if next_div and isinstance(next_div, Tag):
                    endereco = _extract_text_from_tag(next_div)
    return Endereco(endereco_profissional=endereco)


def _extract_resumo(soup: BeautifulSoup) -> str:
    """
    Extracts the summary.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        str: Summary text.
    """
    summary_tag = soup.find("p", class_="resumo")
    summary = (
        _extract_text_from_tag(summary_tag) if isinstance(summary_tag, Tag) else ""
    )
    summary = re.sub(
        r"\s*\((?:Texto informado pelo autor)\)\s*$", "", summary, flags=re.IGNORECASE
    )
    return summary


def _extract_formacao_academica(soup: BeautifulSoup) -> list[Formacao]:
    """
    Extracts academic formations.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        list[Formacao]: List of academic formations.
    """
    formations: list[Formacao] = []
    container = _find_anchor_and_container(
        soup, "FormacaoAcademicaTitulacao", "layout-cell-12"
    )
    if container is None:
        return formations

    period_divs = container.find_all("div", class_="layout-cell-3", recursive=False)
    for period_div in period_divs:
        if not isinstance(period_div, Tag):
            continue
        desc_div = period_div.find_next_sibling("div", class_="layout-cell-9")
        if desc_div is None or not isinstance(desc_div, Tag):
            continue
        # Remove tooltips
        tooltip = desc_div.find("a", class_="tooltip-oasis")
        if isinstance(tooltip, Tag):
            tooltip.decompose()
        description = _extract_text_from_tag(desc_div)
        period = _extract_text_from_tag(period_div)

        # Determine formation type based on keywords
        tipo = "Não identificado"
        if "Doutorado" in description:
            tipo = "Doutorado"
        elif "Mestrado" in description:
            tipo = "Mestrado"
        elif "Especialização" in description:
            tipo = "Especialização"
        elif "Graduação" in description:
            tipo = "Graduação"
        elif "Pós-Doutorado" in description or "Pós-doutorado" in description:
            tipo = "Pós-doutorado"
        elif "Aperfeiçoamento" in description:
            tipo = "Aperfeiçoamento"
        elif "Curso técnico/profissionalizante" in description:
            tipo = "Técnico/Profissionalizante"

        # Extract titulo
        titulo = None
        titulo_match = re.search(r"Título:\s*([^.]+)", description)
        if titulo_match:
            titulo = titulo_match.group(1).strip()

        # Extract orientador
        orientador = None
        orientador_match = re.search(r"Orientador:\s*([^.]+)", description)
        if orientador_match:
            orientador = orientador_match.group(1).strip()

        # Extract bolsa
        bolsa = None
        bolsa_match = re.search(r"Bolsista do\(a\):\s*([^.]+)", description)
        if bolsa_match:
            bolsa = bolsa_match.group(1).strip()

        formations.append(
            Formacao(
                periodo=period,
                tipo_formacao=tipo,
                descricao_formacao=description,
                titulo=titulo,
                orientador=orientador,
                bolsa=bolsa,
            )
        )
    return formations


def _extract_pos_doutorado(soup: BeautifulSoup) -> list[PosDoutorado]:
    """
    Extracts post-doctoral information.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        list[PosDoutorado]: List of post-doctoral experiences.
    """
    pos_doutorados: list[PosDoutorado] = []
    container = _find_anchor_and_container(
        soup, "FormacaoAcademicaPosDoutorado", "layout-cell-12"
    )
    if container is None:
        return pos_doutorados

    period_divs = container.find_all("div", class_="layout-cell-3", recursive=False)
    for period_div in period_divs:
        if not isinstance(period_div, Tag):
            continue
        desc_div = period_div.find_next_sibling("div", class_="layout-cell-9")
        if desc_div is None or not isinstance(desc_div, Tag):
            continue
        description = _extract_text_from_tag(desc_div)
        period = _extract_text_from_tag(period_div)
        pos_doutorados.append(PosDoutorado(periodo=period, descricao=description))
    return pos_doutorados


def _extract_formacao_complementar(soup: BeautifulSoup) -> list[FormacaoComplementar]:
    """
    Extracts complementary formations.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        list[FormacaoComplementar]: List of complementary formations.
    """
    complementares: list[FormacaoComplementar] = []
    container = _find_anchor_and_container(
        soup, "FormacaoComplementar", "layout-cell-12"
    )
    if container is None:
        return complementares

    period_divs = container.find_all("div", class_="layout-cell-3", recursive=False)
    for period_div in period_divs:
        if not isinstance(period_div, Tag):
            continue
        desc_div = period_div.find_next_sibling("div", class_="layout-cell-9")
        if desc_div is None or not isinstance(desc_div, Tag):
            continue
        description = _extract_text_from_tag(desc_div)
        period = _extract_text_from_tag(period_div)
        complementares.append(
            FormacaoComplementar(periodo=period, descricao=description)
        )
    return complementares


def _extract_atuacao_profissional(soup: BeautifulSoup) -> list[VinculoInstitucional]:
    """
    Extracts professional activities with granular details.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        list[VinculoInstitucional]: List of professional activities.
    """
    vinculos: list[VinculoInstitucional] = []
    container = _find_anchor_and_container(
        soup, "AtuacaoProfissional", "layout-cell-12"
    )
    if container is None:
        return vinculos

    inst_backs = container.find_all("div", class_="inst_back")
    for inst_back in inst_backs:
        if not isinstance(inst_back, Tag):
            continue
        instituicao_tag = inst_back.find("b")
        instituicao = (
            _extract_text_from_tag(instituicao_tag)
            if isinstance(instituicao_tag, Tag)
            else ""
        )

        # Find the next elements after inst_back
        current = inst_back
        vinculo_data = {}
        atividades = []

        while True:
            current = current.find_next_sibling()
            if current is None or (
                isinstance(current, Tag) and current.get("class") == ["inst_back"]
            ):
                break
            if not isinstance(current, Tag):
                continue

            if current.get("class") == [
                "layout-cell",
                "layout-cell-3",
                "text-align-right",
            ]:
                periodo = _extract_text_from_tag(current)
                desc_div = current.find_next_sibling("div", class_="layout-cell-9")
                if desc_div and isinstance(desc_div, Tag):
                    descricao = _extract_text_from_tag(desc_div)
                    if "Vínculo:" in descricao:
                        # This is a main vinculo
                        vinculo_match = re.search(r"Vínculo:\s*([^,]+)", descricao)
                        enquadramento_match = re.search(
                            r"Enquadramento Funcional:\s*([^,]+)", descricao
                        )
                        carga_match = re.search(r"Carga horária:\s*([^,]+)", descricao)
                        regime_match = re.search(r"Regime:\s*([^.]+)", descricao)
                        vinculo_data = {
                            "instituicao": instituicao,
                            "periodo": periodo,
                            "vinculo": vinculo_match.group(1).strip()
                            if vinculo_match
                            else "",
                            "enquadramento": enquadramento_match.group(1).strip()
                            if enquadramento_match
                            else "",
                            "carga_horaria": carga_match.group(1).strip()
                            if carga_match
                            else None,
                            "regime": regime_match.group(1).strip()
                            if regime_match
                            else None,
                            "atividades": [],
                        }
                    else:
                        # This is an activity
                        cargo_match = re.search(r"Cargo ou função\s*(.+)", descricao)
                        disciplinas = []
                        linhas = []
                        if "Disciplinas ministradas" in descricao:
                            disc_match = re.search(
                                r"Disciplinas ministradas\s*(.+?)(?=Linhas de pesquisa|$)",
                                descricao,
                                re.DOTALL,
                            )
                            if disc_match:
                                disc_text = disc_match.group(1).strip()
                                disciplinas = [
                                    d.strip()
                                    for d in re.split(
                                        r'<br class="clear">|;', disc_text
                                    )
                                    if d.strip()
                                ]
                        if "Linhas de pesquisa" in descricao:
                            linha_match = re.search(
                                r"Linhas de pesquisa\s*(.+)", descricao, re.DOTALL
                            )
                            if linha_match:
                                linha_text = linha_match.group(1).strip()
                                linhas = [
                                    linha.strip()
                                    for linha in re.split(
                                        r'<br class="clear">|;', linha_text
                                    )
                                    if linha.strip()
                                ]
                        atividade = AtividadeProfissional(
                            periodo=periodo,
                            descricao=descricao,
                            cargo_funcao=cargo_match.group(1).strip()
                            if cargo_match
                            else None,
                            disciplinas_ministradas=disciplinas,
                            linhas_pesquisa=linhas,
                        )
                        if vinculo_data:
                            vinculo_data["atividades"].append(atividade)
                        else:
                            atividades.append(atividade)

        if vinculo_data:
            vinculos.append(VinculoInstitucional(**vinculo_data))

    return vinculos


def _extract_projetos(soup: BeautifulSoup, anchor: str) -> list[Projeto]:
    """
    Extracts projects (research or extension).

    Args:
        soup (BeautifulSoup): The parsed HTML.
        anchor (str): Anchor name for the section.

    Returns:
        list[Projeto]: List of projects.
    """
    projetos: list[Projeto] = []
    container = _find_anchor_and_container(soup, anchor, "layout-cell-12")
    if container is None:
        return projetos

    period_divs = container.find_all("div", class_="layout-cell-3")
    desc_divs = container.find_all("div", class_="layout-cell-9")
    for period_div, desc_div in zip(period_divs, desc_divs):
        if not isinstance(period_div, Tag) or not isinstance(desc_div, Tag):
            continue
        lines = [line.strip() for line in desc_div.stripped_strings]
        titulo = lines[0] if lines else "Título não encontrado"
        if titulo.startswith("Periódico:") or titulo.startswith("Grande área:"):
            continue
        full_desc = " ".join(lines)
        status_match = re.search(r"Situação:\s*([^;]+);", full_desc)
        nature_match = re.search(r"Natureza:\s*([^.]+)\.", full_desc)
        integrantes_match = re.search(r"Integrantes:\s*([^|]+)", full_desc)
        integrantes = []
        if integrantes_match:
            colaboradores_text = integrantes_match.group(1).strip().replace(".", "")
            for collab in colaboradores_text.split("/"):
                name = collab.split(" - ")[0].strip()
                if name:
                    integrantes.append(name)
        projetos.append(
            Projeto(
                periodo=_extract_text_from_tag(period_div),
                titulo=titulo,
                situacao=status_match.group(1).strip() if status_match else None,
                natureza=nature_match.group(1).strip() if nature_match else None,
                integrantes=integrantes,
            )
        )
    return projetos


def _extract_producao_bibliografica(soup: BeautifulSoup) -> list[ProducaoBibliografica]:
    """
    Extracts bibliographic production.

    Args:
        soup (BeautifulSoup): The parsed HTML.

    Returns:
        list[ProducaoBibliografica]: List of bibliographic productions.
    """
    producoes: list[ProducaoBibliografica] = []
    container = _find_anchor_and_container(
        soup, "ProducaoBibliografica", "layout-cell-12"
    )
    if container is None:
        return producoes

    items = container.find_all("div", class_="layout-cell-11")
    for item in items:
        if not isinstance(item, Tag):
            continue
        transform_span = item.find("span", class_="transform")
        if transform_span is None:
            continue
        # Remove the informacao-artigo spans to avoid duplicates
        for span in item.find_all("span", class_="informacao-artigo"):
            span.decompose()
        text_clean = _extract_text_from_tag(item)
        text_no_number = re.sub(r"^\d+\.\s*", "", text_clean).strip()
        parts = text_no_number.split(" . ")
        if len(parts) < 2:
            continue
        autores_text = parts[0]
        titulo = parts[1] if len(parts) > 1 else ""
        autores = [autor.strip() for autor in autores_text.split(";") if autor.strip()]
        # Extract year and journal if available
        ano_match = re.search(r"\b(20\d{2})\b", text_clean)
        revista_match = re.search(r"Revista:\s*([^.]+)", text_clean)
        doi_match = re.search(r"DOI:\s*([^\s]+)", text_clean)
        paginas_match = re.search(r"Páginas:\s*([^\s]+)", text_clean)
        producoes.append(
            ProducaoBibliografica(
                titulo=titulo,
                autores=autores,
                ano=ano_match.group(1) if ano_match else None,
                revista=revista_match.group(1).strip() if revista_match else None,
                doi=doi_match.group(1).strip() if doi_match else None,
                paginas=paginas_match.group(1).strip() if paginas_match else None,
            )
        )
    return producoes


def extract_professor_data(content_html: str) -> ProfessorData | None:
    """
    Main function to extract all data from a single CV HTML.

    Args:
        content_html (str): The HTML content as a string.

    Returns:
        ProfessorData | None: Extracted data or None if error.
    """
    try:
        soup = BeautifulSoup(content_html, "lxml")
        identificacao = _extract_identificacao(soup)
        endereco = _extract_endereco(soup)
        resumo = _extract_resumo(soup)
        formacao_academica = _extract_formacao_academica(soup)
        pos_doutorado = _extract_pos_doutorado(soup)
        formacao_complementar = _extract_formacao_complementar(soup)
        atuacao_profissional = _extract_atuacao_profissional(soup)
        projetos_pesquisa = _extract_projetos(soup, "ProjetosPesquisa")
        projetos_extensao = _extract_projetos(soup, "ProjetosExtensao")
        producao_bibliografica = _extract_producao_bibliografica(soup)
        citation_names = set(identificacao.nomes_citacao)
        coautores = _extract_coauthors(soup, citation_names)
        colaboradores = _extract_project_collaborators(soup, identificacao.nome)

        return ProfessorData(
            identificacao=identificacao,
            endereco=endereco,
            resumo=resumo,
            formacao_academica=formacao_academica,
            pos_doutorado=pos_doutorado,
            formacao_complementar=formacao_complementar,
            atuacao_profissional=atuacao_profissional,
            projetos_pesquisa=projetos_pesquisa,
            projetos_extensao=projetos_extensao,
            producao_bibliografica=producao_bibliografica,
            coautores_publicacoes=coautores,
            colaboradores_projetos=colaboradores,
        )
    except Exception as e:
        logging.error(f"Erro inesperado ao extrair dados: {e}")
        return None


def process_directory(input_dir: str) -> list[ProfessorData]:
    """
    Processes all HTML files in the input directory.

    Args:
        input_dir (str): Path to the directory containing HTML files.

    Returns:
        list[ProfessorData]: List of extracted professor data.
    """
    html_files = [f for f in os.listdir(input_dir) if f.endswith(".html")]
    logging.info(
        f"Iniciando processamento de {len(html_files)} arquivos HTML em '{input_dir}'..."
    )
    extracted_data: list[ProfessorData] = []

    for i, filename in enumerate(html_files):
        filepath = os.path.join(input_dir, filename)
        logging.info(f"({i + 1}/{len(html_files)}) Processando: {filename}")
        try:
            with open(filepath, encoding="utf-8") as file:
                content = file.read()
            extracted = extract_professor_data(content)
            if extracted and extracted.identificacao.nome:
                extracted_data.append(extracted)
            else:
                logging.warning(f"Nenhum dado extraído de {filename}.")
        except Exception as e:
            logging.error(f"Erro ao processar {filename}: {e}")

    logging.info("Processamento concluído!")
    return extracted_data


def main() -> None:
    """
    Main entry point: Parses arguments, processes files, and saves output.
    """

    parser = argparse.ArgumentParser(
        description="Processa currículos Lattes em HTML. Salva em JSON granular."
    )
    parser.add_argument("--input", required=True, help="Diretório com arquivos HTML.")
    parser.add_argument(
        "--output",
        required=True,
        help="Caminho de saída (deve ser .json).",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.input):
        logging.error(f"Diretório de entrada inválido: {args.input}")
        return

    extracted_data = process_directory(args.input)
    if not extracted_data:
        logging.warning("Nenhum dado extraído.")
        return

    output_path = args.output
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    _, ext = os.path.splitext(output_path)
    ext = ext.lower()

    if ext != ".json":
        logging.error("A saída deve ser um arquivo .json para manter a granularidade.")
        return

    try:
        data = [asdict(prof) for prof in extracted_data]
        data.sort(key=lambda x: x["identificacao"]["nome"])
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(
            f"Dados salvos em '{output_path}' ({len(extracted_data)} professores)."
        )
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo: {e}")


if __name__ == "__main__":
    main()
