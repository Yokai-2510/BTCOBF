import csv
import json
from pathlib import Path

from delta_rest_client import DeltaRestClient

credentials_path = Path("source/credentials.json")

if not credentials_path.exists():
    raise FileNotFoundError(
        "Missing source/credentials.json. Copy source/credentials_example.json "
        "to source/credentials.json and add your Delta Exchange credentials."
    )

with credentials_path.open() as f:
    credentials = json.load(f)

delta_client = DeltaRestClient(
    base_url=credentials['delta_exchange']['base_url'],
    api_key=credentials['delta_exchange']['api_key'],
    api_secret=credentials['delta_exchange']['api_secret']
)

assets_list = delta_client.get_assets()

# --- WRITE CSV ---
with open("assets.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=assets_list[0].keys())
    writer.writeheader()
    writer.writerows(assets_list)

print("CSV created: assets.csv")
