import unicodedata
import re


def tem_formacao(prof, nivel):
    for f in prof.get("formacao_academica", []):
        desc = f.get("tipo_formacao", "").lower()
        if nivel in desc:
            return "sim"
    return "não"


def calcular_anos_experiencia(prof):
    anos = []
    for f in prof.get("formacao_academica", []):
        tipo = f.get("tipo_formacao", "").lower()
        # Procura por graduação
        if "graduação" in tipo or "graduacao" in tipo:
            # Tenta pegar o ano de conclusão
            ano = f.get("ano_conclusao")
            if ano and str(ano).isdigit():
                anos.append(int(ano))
            else:
                # Alternativamente, tenta extrair do campo 'periodo'
                periodo = f.get("periodo", "")
                if " - " in periodo:
                    partes = periodo.split(" - ")
                    if len(partes) > 1 and partes[1].isdigit():
                        anos.append(int(partes[1]))
    if anos:
        return 2025 - min(anos)
    return None


def normalizar_nome_citacao(nome):
    # Remove acentos
    nome = unicodedata.normalize("NFKD", nome)
    nome = "".join([c for c in nome if not unicodedata.combining(c)])
    # Remove espaços, pontos e deixa maiúsculo
    return re.sub(r"[\s\.]", "", nome).upper()


def normalizar_coautor(coautor, citacao_para_nome):
    if isinstance(coautor, str):
        chave = normalizar_nome_citacao(coautor)
        return citacao_para_nome.get(chave, coautor.strip())
    return coautor


def quebra_nome(nome, n=18):
    # Quebra o nome a cada n caracteres, preferencialmente em espaços
    partes = []
    atual = ""
    for palavra in nome.split():
        if len(atual) + len(palavra) + 1 > n and atual:
            partes.append(atual)
            atual = palavra
        else:
            atual = atual + " " + palavra if atual else palavra
    if atual:
        partes.append(atual)
    return "\n".join(partes)


def definir_nivel_formacao(row):
    if row["pos_doutorado"] == "sim":
        return "Pós-doutorado"
    elif row["doutorado"] == "sim":
        return "Doutorado"
    elif row["mestrado"] == "sim":
        return "Mestrado"
    else:
        return "Graduação"


def remove_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data >= lower_bound) & (data <= upper_bound)]


def preprocess_text(text, stopwords):
    import string
    import re

    # Minúsculas
    text = text.lower().split(".")[0]
    # Remover pontuação
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remover números
    text = re.sub(r"\d+", "", text)
    # Remover espaços extras
    text = text.strip()
    # Remover stopwords
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords]
    return " ".join(tokens)
