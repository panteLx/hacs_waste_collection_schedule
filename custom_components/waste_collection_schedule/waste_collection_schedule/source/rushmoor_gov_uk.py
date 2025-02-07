import json
from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Rushmoor Borough Council"
DESCRIPTION = "Source for rushmoor.gov.uk services for Rushmoor, UK."
URL = "https://rushmoor.gov.uk"
TEST_CASES = {
    "GU14": {"uprn": "100060551749"},
}

ICON_MAP = {
    "Refuse": "mdi:trash-can",
    "Recycle": "mdi:recycle",
    "Garden": "mdi:leaf",
    "Food": "mdi:food-apple",
}

API_URL = "https://www.rushmoor.gov.uk/Umbraco/Api/BinLookUpWorkAround/Get"


class Source:
    def __init__(self, uprn):
        self._uprn = uprn

    def fetch(self):
        params = {"selectedAddress": self._uprn, "weeks": "16"}
        r = requests.get(API_URL, params=params)
        r.raise_for_status()
        # Douple decode to get rid of the escaped quotes
        data = json.loads(str(r.json()))

        entries = []
        for key, value in data["NextCollection"].items():
            if not key.endswith("Date"):
                continue
            wasteType = key.split("Collection")[0]
            date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").date()
            entries.append(
                Collection(
                    date,
                    wasteType,
                    icon=ICON_MAP.get(wasteType),
                )
            )
        return entries
