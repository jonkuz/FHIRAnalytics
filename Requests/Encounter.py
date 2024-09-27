from datetime import datetime

import requests


def get_encounter(encounter_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Encounter", params={"_id": encounter_id})
    response = res.json()

    # Convert to Datetime object
    period_start = datetime.fromisoformat(response['entry'][0]['resource'].get('period').get('start').replace("Z", "+00:00"))
    period_end = datetime.fromisoformat(response['entry'][0]['resource'].get('period').get('end').replace("Z", "+00:00"))

    return [
        [encounter_id],
        [response['entry'][0]['resource']['identifier'][0].get('value')],
        [response['entry'][0]['resource'].get('status')],
        [response['entry'][0]['resource'].get('class').get('system')],
        [period_start],
        [period_end]
    ]
