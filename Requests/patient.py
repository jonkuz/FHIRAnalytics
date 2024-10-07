from datetime import datetime
import requests
from util import extract_address


def get_patient(patient_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Patient", params={"_id": patient_id})
    patient_response = res.json()
    response = patient_response['entry'][0]['resource']

    identifier_use = []
    identifier_system = []
    identifier_value = []
    for identifier in response['identifier']:
        identifier_use.append(identifier.get('use', ""))
        identifier_system.append(identifier.get('system', ""))
        identifier_value.append(identifier.get('value', ""))

    patient_active = response.get('active', False)

    patient_name_use = []
    patient_text = []
    patient_family = []
    patient_given = []
    for name in response['name']:
        patient_name_use.append(name.get('use', ""))
        patient_text.append(name.get('text', ""))
        patient_family.append(name.get('family'))
        for given in name['given']:
            patient_given.append(given)

    patient_gender = response['gender']
    patient_birth_date = patient_response['entry'][0]['resource'].get('birthDate', None)
    if patient_birth_date is not None:
        patient_birth_date = datetime.fromisoformat(patient_response['entry'][0]['resource']['birthDate']
                                                    .replace("Z", "+00:00"))

    address_type, address_line, address_city, address_postal_code, address_country = extract_address(response)

    marital_status_system = ""
    marital_status_code = ""
    for marital_status in response['maritalStatus']['coding']:
        marital_status_system += marital_status['system']
        marital_status_code += marital_status['code']

    return [
        patient_id,
        identifier_use,
        identifier_system,
        identifier_value,
        patient_active,
        patient_name_use,
        patient_text,
        patient_family,
        [patient_given],
        patient_gender,
        patient_birth_date,
        address_type,
        [address_line],
        address_city,
        address_postal_code,
        address_country,
        marital_status_system,
        marital_status_code
    ]
