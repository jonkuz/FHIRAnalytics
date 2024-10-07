def extract_address(response: dict) -> tuple[list, list, list, list, list]:
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

    return address_type, address_line, address_city, address_postal_code, address_country
