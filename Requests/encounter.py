from datetime import datetime

import requests


def get_encounter(encounter_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Encounter", params={"_id": encounter_id})
    encounter_response = res.json()

    response = encounter_response['entry'][0]['resource']

    identifier_system = []
    identifier_code = []
    identifier_value = []
    for identifier in response['identifier']:
        identifier_system.append(identifier.get('system', ""))
        identifier_code.append(identifier.get('use', ""))
        identifier_value.append(identifier.get('value', ""))

    status = response.get('status', None)
    encounter_class = response.get('class', []).get('system', "")

    # Convert to Datetime object
    period_start = datetime.fromisoformat(response.get('period').get('start').replace("Z", "+00:00"))
    period_end = datetime.fromisoformat(response.get('period').get('end').replace("Z", "+00:00"))

    return [
        encounter_id,
        identifier_system,
        identifier_code,
        identifier_value,
        status,
        encounter_class,
        period_start,
        period_end
    ]
