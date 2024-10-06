import requests


def get_organization(organization_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/Organization", params={"_id": organization_id})
    organization_response = res.json()

    response = organization_response['entry'][0]['resource']

    identifier_system = []
    identifier_value = []
    for identifier in response['identifier']:
        identifier_system.append(identifier.get('system', ""))
        identifier_value.append(identifier.get('value', ""))

    type_system = []
    type_code = []
    for t in response['type']:
        for coding in t['coding']:
            type_system.append(coding.get('system', ""))
            type_code.append(coding.get('code', ""))

    name = response.get('name', "")
    active = response.get('active', False)

    address_type = []
    address_line = []
    address_city = []
    address_postal_code = []
    address_country = []
    for address in response['address']:
        address_type.append(address.get('type', ""))
        for line in address['line']:
            address_line.append(line)
        address_city.append(address.get('city', ""))
        address_postal_code.append(address.get('postalCode', ""))
        address_country.append(address.get('country', ""))

    return [
        organization_id,
        name,
        active,
        identifier_system,
        identifier_value,
        type_system,
        type_code,
        address_type,
        [address_line],
        address_city,
        address_postal_code,
        address_country
    ]

