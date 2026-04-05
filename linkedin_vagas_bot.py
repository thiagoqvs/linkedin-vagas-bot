#!/usr/bin/env python3
"""
LinkedIn Vagas Bot
---------------------------------

from __future__ import annotations

import csv
import math
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus


@dataclass
class SearchConfig:
    roles: list[str] = field(default_factory=lambda: [
        "Engenheiro de Dados Júnior",
        "Analista de Dados Júnior",
        "Estágio em Engenharia de Dados",
        "Estágio em Dados",
        "Data Engineer Junior",
        "Junior Data Engineer",
        "Data Analyst Junior",
    ])

    include_keywords: list[str] = field(default_factory=lambda: [
        "SQL",
        "Python",
        "ETL",
        "AWS",
        "Power BI",
        "Pipeline de Dados",
    ])

    exclude_keywords: list[str] = field(default_factory=lambda: [
        "Senior",
        "Sênior",
        "Pleno",
        "Lead",
        "Especialista",
        "Staff",
        "Manager",
        "Java",
        "C#",
        "SAP",
        "Oracle DBA",
        "Arquiteto",
    ])

    location: str = "Brasil"
    remote_filter: str = "2"
    experience_levels: list[str] = field(default_factory=lambda: ["1", "2"])
    batch_size: int = 3
    output_dir: Path = Path("saida_linkedin_bot")
    force_chrome: bool = False
    chrome_path: str = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"


CONFIG = SearchConfig()


def build_search_phrase(role: str, include_keywords: Iterable[str], exclude_keywords: Iterable[str]) -> str:
    positive = " ".join(include_keywords)
    negative = " ".join(f"-{kw}" if " " not in kw else f'-"{kw}"' for kw in exclude_keywords)
    return f'"{role}" {positive} {negative}'.strip()


def linkedin_jobs_url(search_phrase: str, location: str, remote_filter: str, experience_levels: list[str]) -> str:
    exp = ",".join(experience_levels)
    query = quote_plus(search_phrase)
    loc = quote_plus(location)

    return (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={query}"
        f"&location={loc}"
        f"&f_WT={remote_filter}"
        f"&f_E={exp}"
        f"&sortBy=DD"
    )


def generate_searches(config: SearchConfig) -> list[dict[str, str]]:
    searches: list[dict[str, str]] = []

    for role in config.roles:
        phrase = build_search_phrase(role, config.include_keywords, config.exclude_keywords)
        url = linkedin_jobs_url(
            search_phrase=phrase,
            location=config.location,
            remote_filter=config.remote_filter,
            experience_levels=config.experience_levels,
        )
        searches.append({
            "cargo": role,
            "busca": phrase,
            "url": url,
        })

    return searches


def save_txt(searches: list[dict[str, str]], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    txt_path = output_dir / "links_busca_linkedin.txt"

    with txt_path.open("w", encoding="utf-8") as f:
        for item in searches:
            f.write(f"Cargo: {item['cargo']}\n")
            f.write(f"Busca: {item['busca']}\n")
            f.write(f"URL: {item['url']}\n")
            f.write("-" * 80 + "\n")

    return txt_path


def save_csv(searches: list[dict[str, str]], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "links_busca_linkedin.csv"

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cargo", "busca", "url"])
        writer.writeheader()
        writer.writerows(searches)

    return csv_path


def print_searches(searches: list[dict[str, str]]) -> None:
    print("\nBuscas geradas:\n")
    for i, item in enumerate(searches, start=1):
        print(f"[{i}] {item['cargo']}")
        print(f"    Busca: {item['busca']}")
        print(f"    URL  : {item['url']}\n")


def print_batches(searches: list[dict[str, str]], batch_size: int) -> None:
    total_batches = math.ceil(len(searches) / batch_size)
    print(f"\nTotal de buscas: {len(searches)}")
    print(f"Tamanho do lote: {batch_size}")
    print(f"Total de lotes : {total_batches}\n")

    for batch_number in range(total_batches):
        start = batch_number * batch_size
        end = start + batch_size
        batch = searches[start:end]
        print(f"Lote {batch_number + 1}:")
        for item in batch:
            print(f" - {item['cargo']}")
        print()


def get_browser(config: SearchConfig):
    if config.force_chrome:
        try:
            return webbrowser.get(config.chrome_path)
        except webbrowser.Error:
            print("\nNão foi possível abrir o Chrome pelo caminho configurado.")
            print("Usando navegador padrão do sistema.\n")
    return webbrowser


def open_batch(searches: list[dict[str, str]], batch_size: int, batch_number: int, config: SearchConfig) -> int:
    if batch_size <= 0:
        raise ValueError("batch_size precisa ser maior que zero.")

    total_batches = math.ceil(len(searches) / batch_size)

    if batch_number < 1 or batch_number > total_batches:
        print(f"Lote inválido. Escolha entre 1 e {total_batches}.")
        return 0

    start = (batch_number - 1) * batch_size
    end = start + batch_size
    batch = searches[start:end]

    browser = get_browser(config)
    opened = 0

    for item in batch:
        browser.open_new_tab(item["url"])
        opened += 1

    return opened


def choose_batch_size(default_value: int) -> int:
    print("\nEscolha o tamanho do lote:")
    print("1 - Abrir 3 buscas por vez")
    print("2 - Abrir 5 buscas por vez")
    print("3 - Usar valor padrão do script")
    option = input("Opção: ").strip()

    if option == "1":
        return 3
    if option == "2":
        return 5
    return default_value


def main() -> int:
    searches = generate_searches(CONFIG)

    print("=" * 72)
    print("LINKEDIN VAGAS BOT")
    print("=" * 72)
    print("1 - Mostrar buscas")
    print("2 - Salvar links em TXT e CSV")
    print("3 - Mostrar lotes disponíveis")
    print("4 - Abrir um lote específico no navegador")
    print("5 - Fazer tudo")
    print("0 - Sair")
    print("=" * 72)

    choice = input("Escolha uma opção: ").strip()

    if choice == "0":
        print("Saindo.")
        return 0

    if choice in {"1", "5"}:
        print_searches(searches)

    if choice in {"2", "5"}:
        txt_path = save_txt(searches, CONFIG.output_dir)
        csv_path = save_csv(searches, CONFIG.output_dir)
        print("\nArquivos salvos em:")
        print(f"- {txt_path.resolve()}")
        print(f"- {csv_path.resolve()}")

    if choice in {"3", "4", "5"}:
        batch_size = choose_batch_size(CONFIG.batch_size)
        print_batches(searches, batch_size)

        if choice in {"4", "5"}:
            batch_number_str = input("Qual lote deseja abrir? ").strip()
            if not batch_number_str.isdigit():
                print("Digite um número válido de lote.")
                return 1

            batch_number = int(batch_number_str)
            opened = open_batch(searches, batch_size, batch_number, CONFIG)
            print(f"\n{opened} busca(s) aberta(s) no navegador.")

    if choice not in {"1", "2", "3", "4", "5"}:
        print("Opção inválida.")
        return 1

    print("\nDicas:")
    print("- Ajuste roles/include_keywords/exclude_keywords no bloco CONFIG.")
    print("- Use lote 3 para navegar com mais leveza.")
    print("- Use lote 5 quando quiser acelerar.")
    print("- Depois salve buscas úteis no próprio LinkedIn para criar alertas.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        raise SystemExit(130)
