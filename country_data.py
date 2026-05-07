import csv
from pathlib import Path

COUNTRY_COORDS = {}

csv_path = Path(__file__).parent / "Downloads" / "archive" / "country-coordinates-world.csv"
if csv_path.exists():
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                country = row['Country'].strip()
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                COUNTRY_COORDS[country] = (lat, lon)
            except:
                pass

NATION_CODE_TO_COUNTRY = {
    "USA": "United States of America",
    "RUS": "Russia",
    "CHN": "China",
    "UK":  "United Kingdom",
    "FRA": "France",
    "IND": "India",
    "PAK": "Pakistan",
    "ISR": "Israel",
    "PRK": "North Korea",
}

def get_nation_coords(code):
    country_name = NATION_CODE_TO_COUNTRY.get(code)
    if country_name and country_name in COUNTRY_COORDS:
        return COUNTRY_COORDS[country_name]
    return None
