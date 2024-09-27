from datetime import datetime

import requests


def get_condition(condition_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Condition", params={"_id": condition_id})
    condition_response = res.json()

    con_id = condition_response['entry'][0]['resource']['id']

    identifier_system = ""
    identifier_value = ""
    identifier_use = ""
    for identifier in condition_response['entry'][0]['resource']['identifier']:
        identifier_system += identifier['system']
        identifier_value += identifier['value']
        identifier_use += identifier['use']

    meta_version_id = condition_response['entry'][0]['resource']['meta']['versionId']
    meta_last_updated = datetime.fromisoformat(condition_response['entry'][0]['resource']['meta']['lastUpdated']
                                                  .replace("Z", "+00:00"))


    clinical_status = condition_response['entry'][0]['resource']['clinicalStatus']
    clinical_status_system = ""
    clinical_status_code = ""
    for coding in clinical_status:
        clinical_status_system += coding['system']
        clinical_status_code += coding['code']


    code = condition_response['entry'][0]['resource']['code']
    code_system = ""
    code_version = ""
    code_code = ""
    for coding in code:
        code_system += coding['system']
        code_version += coding['version']
        code_code += coding['code']

    patient_id = condition_response['entry'][0]['resource']['patient']['reference'].split('/')[1]
    encounter = condition_response['entry'][0]['resource']['encounter']['reference'].split('/')[1]
    recorded_date = datetime.fromisoformat(condition_response['entry'][0]['resource']['recordedDate']
                                          .get('start')
                                          .replace("Z", "+00:00"))

    return [[condition_id], [[identifier_system]], [[identifier_value]], [[identifier_use]], [meta_version_id],
                 [meta_last_updated], [clinical_status_system], [clinical_status_code], [code_system], [code_version],
                 [code_code], [patient_id], [encounter], [recorded_date]]

