import requests


def get_medication(medication_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Medication", params={"_id": medication_id})
    response = res.json()

    medication_id = response['entry'][0]['resource']['id']

    identifier_value = ""
    for identifier in response['entry'][0]['resource']['identifier']:
        identifier_value += identifier['value']

    code_system = ""
    code_code = ""
    code_display = ""
    for coding in response['entry'][0]['resource']['code']['coding']:
        code_system += coding['system']
        code_code += coding['code']
        code_display += coding['display']

    status = response['entry'][0]['resource']['status']
    manufacturer = response['entry'][0]['resource']['manufacturer']['reference'].split('/')[1]

    amount_numerator_code = response['entry'][0]['resource']['amount']['numerator'].get('code')
    amount_numerator_unit = response['entry'][0]['resource']['amount']['numerator'].get('unit')
    amount_numerator_system = response['entry'][0]['resource']['amount']['numerator'].get('system')
    amount_numerator_value = response['entry'][0]['resource']['amount']['numerator'].get('value')

    amount_denominator_code = response['entry'][0]['resource']['amount']['denominator'].get('code')
    amount_denominator_unit = response['entry'][0]['resource']['amount']['denominator'].get('unit')
    amount_denominator_system = response['entry'][0]['resource']['amount']['denominator'].get('system')
    amount_denominator_value = response['entry'][0]['resource']['amount']['denominator'].get('value')

    medication = [
        [medication_id],
        [identifier_value],
        [[code_system]],
        [[code_code]],
        [[code_display]],
        [status],
        [manufacturer],
        [amount_numerator_code],
        [amount_numerator_unit],
        [amount_numerator_system],
        [amount_numerator_value],
        [amount_denominator_code],
        [amount_denominator_unit],
        [amount_denominator_system],
        [amount_denominator_value]
    ]
    return medication
