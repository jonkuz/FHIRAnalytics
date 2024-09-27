import requests


def get_organization(organization_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Organization", params={"_id": organization_id})
    orga_response = res.json()

    orga_id = orga_response['entry'][0]['resource']['id']

    identifier_system = ""
    identifier_value = ""
    for identifier in orga_response['entry'][0]['resource']['identifier']:
        identifier_system += identifier['system']
        identifier_value += identifier['value']

    type_system = ""
    type_code = ""
    for t in orga_response['entry'][0]['resource']['type']:
        for coding in t['coding']:
            type_system += coding['system']
            type_code += coding['code']

    name = orga_response['entry'][0]['resource']['name']
    active = orga_response['entry'][0]['resource']['active']

    address_type = ""
    address_line = ""
    address_city = ""
    address_postal_code = ""
    address_country = ""
    for address in orga_response['entry'][0]['resource']['address']:
        address_type += address['type']
        for line in address['line']:
            address_line += line
        address_city += address['city']
        address_postal_code += address['postalCode']
        address_country += address['country']

    return [[orga_id], [name], [active], [[identifier_system]], [[identifier_value]], [[type_system]], [[type_code]], [address_type], [[address_line]], [address_city], [address_postal_code], [address_country]]

