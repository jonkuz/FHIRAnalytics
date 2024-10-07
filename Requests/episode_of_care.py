from datetime import datetime
import requests


def get_episode_of_care(episode_of_care_id: int) -> list:
    res = requests.get("http://localhost:8080/fhir/EpisodeOfCare", params={"_id": episode_of_care_id})
    eoc_response = res.json()
    response = eoc_response['entry'][0]['resource']

    identifier_value = []
    for identifier in response['identifier']:
        identifier_value.append(identifier.get('value', ""))

    status = response.get('status', None)
    managing_organization = response['managingOrganization']['reference'].split('/')[1]

    period_end = response['period'].get('end', None)
    if period_end is not None:
        period_end = datetime.fromisoformat(eoc_response['entry'][0]['resource']['period']
                                            .get('end', None)
                                            .replace("Z", "+00:00"))

    period_start = datetime.fromisoformat(eoc_response['entry'][0]['resource']['period']
                                          .get('start')
                                          .replace("Z", "+00:00"))

    return [
        episode_of_care_id,
        identifier_value,
        status,
        managing_organization,
        period_start,
        period_end
    ]
