from playwright.sync_api import sync_playwright, Playwright
import pandas as pd
import os
import argparse


def salvar_div_como_html(page, arquivo: str, diretorio: str):
    # Aguarda o seletor da div e pega o conteúdo HTML
    page.wait_for_selector("xpath=/html/body/div[1]/div[3]/div/div/div", timeout=20000)
    conteudo = page.inner_html("xpath=/html/body/div[1]/div[3]/div/div/div")
    os.makedirs(diretorio, exist_ok=True)
    arquivo_final = os.path.join(diretorio, arquivo)
    if not os.path.isfile(arquivo_final):
        with open(arquivo_final, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Conteúdo salvo em {arquivo_final}")


def run(playwright: Playwright, url: str, output: str, diretorio: str):
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    print("Página inicial acessada.")
    page.wait_for_selector(
        'xpath=//*[@id="id_form_previw"]/div/div/div[2]/div/div/div/div[2]/ul/li[1]/a',
        timeout=20000,
    )

    with page.expect_popup() as new_page_info:
        page.click(
            'xpath=//*[@id="id_form_previw"]/div/div/div[2]/div/div/div/div[2]/ul/li[1]/a'
        )
    new_page = new_page_info.value
    new_page.wait_for_load_state("load")
    print("Nova página aberta.")
    salvar_div_como_html(new_page, output, diretorio)
    browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Download profiles from Lattes platform"
    )
    parser.add_argument(
        "--input", "-i", required=True, help="CSV file with professors data"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="perfis",
        help="Output directory for downloaded profiles (default: perfis)",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.input)

    for idx, linha in df.iterrows():
        codigo = linha["Código(Busca Textual)"]
        nome = linha["Nome dos Professores"]
        url = f"https://buscatextual.cnpq.br/buscatextual/preview.do?metodo=apresentar&id={codigo}"
        print(idx, url)
        with sync_playwright() as playwright:
            run(playwright, url, nome + ".html", args.output)


if __name__ == "__main__":
    main()
