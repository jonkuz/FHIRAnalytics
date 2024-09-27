from datetime import datetime

import requests


def get_episode_of_care(episode_of_care_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/EpisodeOfCare", params={"_id": episode_of_care_id})
    eoc_response = res.json()

    eoc_id = eoc_response['entry'][0]['resource']['id']

    identifier_type_coding_system = ""
    identifier_type_coding_code = ""
    eoc_identifier_value = ""
    for identifier in eoc_response['entry'][0]['resource']['identifier']:
        eoc_identifier_value += identifier['value']
        for coding in identifier['type']['coding']:
            identifier_type_coding_system += coding['system']
            identifier_type_coding_code += coding['code']

    status = eoc_response['entry'][0]['resource']['status']
    patient_id = eoc_response['entry'][0]['resource']['patient']['reference'].split('/')[1]
    managing_organization = eoc_response['entry'][0]['resource']['managingOrganization']['reference'].split('/')[1]
    period_end = eoc_response['entry'][0]['resource']['period'].get('end', None)
    if period_end is not None:
        period_end = datetime.fromisoformat(eoc_response['entry'][0]['resource']['period']
                                            .get('end', None)
                                            .replace("Z", "+00:00"))

    period_start = datetime.fromisoformat(eoc_response['entry'][0]['resource']['period']
                                          .get('start')
                                          .replace("Z", "+00:00"))

    return [[eoc_id], [[identifier_type_coding_system]], [[identifier_type_coding_code]],
                       [[eoc_identifier_value]], [status], [patient_id],
                       [managing_organization], [period_start], [period_end]]
