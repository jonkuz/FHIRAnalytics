from datetime import datetime

import requests


def get_patient(patient_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Patient", params={"_id": patient_id})
    patient_response = res.json()

    patient_id = patient_response['entry'][0]['resource']['id']
    identifier_use = ""
    identifier_system = ""
    identifier_value = ""
    for identifier in patient_response['entry'][0]['resource']['identifier']:
        identifier_use += identifier['use']
        identifier_system += identifier['system']
        identifier_value += identifier['value']

    patient_active = patient_response['entry'][0]['resource']['active']

    patient_name_use = ""
    patient_family = ""
    patient_given = ""
    for name in patient_response['entry'][0]['resource']['name']:
        patient_name_use += name['use']
        patient_family += name['family']
        for given in name['given']:
            patient_given += given

    patient_gender = patient_response['entry'][0]['resource']['gender']
    patient_birth_date = datetime.fromisoformat(patient_response['entry'][0]['resource']['birthDate']
                                                .replace("Z", "+00:00"))
    address_type = ""
    address_line = ""
    address_city = ""
    address_postal_code = ""
    address_country = ""
    for address in patient_response['entry'][0]['resource']['address']:
        address_type += address['type']
        for line in address['line']:
            address_line += line
        address_city += address['city']
        address_postal_code += address['postalCode']
        address_country += address['country']

    marital_status_system = ""
    marital_status_code = ""
    for marital_status in patient_response['entry'][0]['resource']['maritalStatus']['coding']:
        marital_status_system += marital_status['system']
        marital_status_code += marital_status['code']

    return [
        [patient_id],
        [[identifier_use]],
        [[identifier_system]],
        [[identifier_value]],
        [patient_active],
        [patient_name_use],
        [patient_family],
        [[patient_given]],
        [patient_gender],
        [patient_birth_date],
        [address_type],
        [[address_line]],
        [address_city],
        [address_postal_code],
        [address_country],
        [marital_status_system],
        [marital_status_code]
    ]
