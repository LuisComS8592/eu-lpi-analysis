# src/utils/helpers.py

from typing import List, Dict
import requests
import pandas as pd

def map_country_codes(codes: List[str]) -> Dict[str, str]:
    mapping = {
        'AT': 'Austria',
        'BE': 'Belgium',
        'BG': 'Bulgaria',
        'HR': 'Croatia',
        'CY': 'Cyprus',
        'CZ': 'Czechia',
        'DK': 'Denmark',
        'EE': 'Estonia',
        'FI': 'Finland',
        'FR': 'France',
        'DE': 'Germany',
        'GR': 'Greece',
        'HU': 'Hungary',
        'IE': 'Ireland',
        'IT': 'Italy',
        'LV': 'Latvia',
        'LT': 'Lithuania',
        'LU': 'Luxembourg',
        'MT': 'Malta',
        'NL': 'Netherlands',
        'PL': 'Poland',
        'PT': 'Portugal',
        'RO': 'Romania',
        'SK': 'Slovakia',
        'SI': 'Slovenia',
        'ES': 'Spain',
        'SE': 'Sweden'
    }
    return {code: mapping.get(code, "Unknown") for code in codes}

EU_COUNTRIES = [
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
    'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'
]

LPI_INDICATORS = {
    "Customs": "LP.LPI.CUST.XQ",
    "Infrastructure": "LP.LPI.INFR.XQ",
    "International Shipments": "LP.LPI.ITRN.XQ",
    "Logistics Quality and Competence": "LP.LPI.LOGS.XQ",
    "Tracking and Tracing": "LP.LPI.TRAC.XQ",
    "Timeliness": "LP.LPI.TIME.XQ",
    "LPI Aggregate": "LP.LPI.OVRL.XQ"
}

def fetch_indicator_data(indicator_code: str, indicator_name: str) -> list:
    records = []

    for country_code in EU_COUNTRIES:
        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&date=2007:2023&per_page=1000"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if len(data) > 1 and data[1] is not None:
                for entry in data[1]:
                    if entry.get("value") is not None:
                        records.append({
                            "Country": entry.get("country", {}).get("value"),
                            "Year": int(entry.get("date")),
                            "Indicator": indicator_code,
                            "Indicator Name": indicator_name,
                            "Value": entry.get("value")
                        })
        except (requests.RequestException, ValueError) as e:
            print(f"⚠️ Erro ao baixar dados {indicator_code} para {country_code}: {e}")

    return records

def load_remote_lpi_data() -> pd.DataFrame:
    all_records = []
    for name, code in LPI_INDICATORS.items():
        print(f"🔄 Baixando dados para: {name}")
        data = fetch_indicator_data(code, name)
        all_records.extend(data)

    df = pd.DataFrame(all_records)
    df = df.dropna(subset=["Value"])

    df_pivot = df.pivot_table(
        index=["Country", "Year"],
        columns="Indicator Name",
        values="Value"
    ).reset_index()

    return df_pivot

SUBINDICATORS = [
    "Customs",
    "Infrastructure",
    "International Shipments",
    "Logistics Quality and Competence",
    "Tracking and Tracing",
    "Timeliness"
]
