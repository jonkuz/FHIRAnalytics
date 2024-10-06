import requests


def get_medication(medication_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Medication", params={"_id": medication_id})
    medication_response = res.json()
    response = medication_response['entry'][0]['resource']

    identifier_value = []
    for identifier in response['identifier']:
        identifier_value.append(identifier.get('value', ""))

    code_system = []
    code_code = []
    code_display = []
    for coding in response['code']['coding']:
        code_system.append(coding.get('system', ""))
        code_code.append(coding.get('code', ""))
        code_display.append(coding.get('display', ""))

    status = response.get('status', None)
    manufacturer = response['manufacturer'].get('reference', "").split('/')[1]

    amount_numerator_code = response['amount']['numerator'].get('code')
    amount_numerator_unit = response['amount']['numerator'].get('unit')
    amount_numerator_system = response['amount']['numerator'].get('system')
    amount_numerator_value = response['amount']['numerator'].get('value')

    amount_denominator_code = response['amount']['denominator'].get('code')
    amount_denominator_unit = response['amount']['denominator'].get('unit')
    amount_denominator_system = response['amount']['denominator'].get('system')
    amount_denominator_value = response['amount']['denominator'].get('value')

    return [
        identifier_value,
        code_system,
        code_code,
        code_display,
        status,
        manufacturer,
        amount_numerator_code,
        amount_numerator_unit,
        amount_numerator_system,
        amount_numerator_value,
        amount_denominator_code,
        amount_denominator_unit,
        amount_denominator_system,
        amount_denominator_value
    ]
