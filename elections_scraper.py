import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
elections_scraper.py: Elections Scraper pro Engeto Online Python Akademie
author: Josef Lučan
email: peposh1@seznam.cz
discord: Josef Lučan#98945
"""

def scrape_election_data(url):
    # Načtení obsahu webové stránky
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Chyba při načítání stránky: {response.status_code}")
        return None

    # Zpracování HTML pomocí BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Najdi tabulku s třídou 'table'
    table = soup.find('table', {'class': 'table'})
    if table is None:
        print("Tabulka s volebními výsledky nebyla nalezena.")
        return None

    # Vyber všechny řádky tabulky (kromě hlavičky)
    rows = table.find_all('tr')[1:]  # Vynecháme první řádek s hlavičkou

    # Ulož výsledky
    results = []
    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 6:  # Zkontroluj, že je dostatek sloupců
            continue

        code = columns[0].text.strip()
        name = columns[1].text.strip()
        voters = columns[2].text.strip()
        envelopes = columns[3].text.strip()
        valid_votes = columns[4].text.strip()

        # Hlasování pro strany - sloupce od 5 dál
        parties_votes = [col.text.strip() for col in columns[5:]]

        results.append({
            'Kód obce': code,
            'Název obce': name,
            'Voliči v seznamu': voters,
            'Vydané obálky': envelopes,
            'Platné hlasy': valid_votes,
            'Hlasování pro strany': parties_votes
        })

    return results

def save_to_csv(data, filename):
    # Vytvoř DataFrame a ulož ho jako CSV
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8', sep=';')  # Použití středníku jako oddělovače
    print(f"Data byla úspěšně uložena do {filename}")

def main():
    parser = argparse.ArgumentParser(description='Scrape volební výsledky zadaného územního celku.')
    parser.add_argument('url', help='URL územního celku pro scraping')
    parser.add_argument('output', help='Jméno výstupního souboru (např. vysledky.csv)')

    args = parser.parse_args()

    # Validace URL
    if 'volby.cz' not in args.url:
        print("Chybný URL odkaz. Zadejte správný odkaz na volby.cz.")
        return

    # Scraping dat
    election_data = scrape_election_data(args.url)
    if election_data:
        save_to_csv(election_data, args.output)

if __name__ == "__main__":
    main()
